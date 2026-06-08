#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <signal.h>

#define MAX_LINE 1024
#define MAX_ARGS 64
#define MAX_BG_PROCS 128

static pid_t bg_pids[MAX_BG_PROCS];
static int bg_count = 0;

void sigchld_handler(int sig) {
  (void)sig;
  while (1) {
    int wstatus;
    pid_t pid = waitpid(-1, &wstatus, WNOHANG);
    if (pid <= 0) break;
    for (int i = 0; i < bg_count; i++) {
      if (bg_pids[i] == pid) {
        for (int j = i; j < bg_count - 1; j++)
          bg_pids[j] = bg_pids[j + 1];
        bg_count--;
        break;
      }
    }
  }
}

void setup_signal_handlers(void) {
  struct sigaction sa;
  sa.sa_handler = sigchld_handler;
  sigemptyset(&sa.sa_mask);
  sa.sa_flags = SA_RESTART | SA_NOCLDSTOP;
  sigaction(SIGCHLD, &sa, NULL);
}

int tokenize(char *line, char **args) {
  int count = 0;
  char *p = line;
  while (*p) {
    while (*p == ' ' || *p == '\t') *p++ = '\0';
    if (*p == '\0') break;
    if (*p == '"') {
      p++;
      args[count++] = p;
      while (*p && *p != '"') p++;
      if (*p) *p++ = '\0';
    } else {
      args[count++] = p;
      while (*p && *p != ' ' && *p != '\t') p++;
    }
  }
  args[count] = NULL;
  return count;
}

int handle_builtin(char **args, int argc) {
  if (argc == 0) return 0;

  if (strcmp(args[0], "exit") == 0) {
    exit(0);
  }

  if (strcmp(args[0], "cd") == 0) {
    const char *path = args[1] ? args[1] : getenv("HOME");
    if (path == NULL) path = "/";
    if (chdir(path) != 0)
      perror("cd");
    return 1;
  }

  if (strcmp(args[0], "pwd") == 0) {
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)))
      puts(cwd);
    return 1;
  }

  if (strcmp(args[0], "jobs") == 0) {
    if (bg_count == 0) {
      puts("No background jobs.");
    } else {
      for (int i = 0; i < bg_count; i++)
        printf("[%d] %d\n", i + 1, bg_pids[i]);
    }
    return 1;
  }

  if (strcmp(args[0], "help") == 0) {
    puts("Mini Shell -- built-in commands:");
    puts("  cd [dir]    Change directory");
    puts("  pwd         Print working directory");
    puts("  exit        Exit shell");
    puts("  jobs        List background jobs");
    puts("  help        Show this help");
    puts("  &           Run command in background");
    puts("  |           Pipe between commands");
    puts("  > file      Redirect stdout to file");
    puts("  < file      Redirect stdin from file");
    return 1;
  }

  return 0;
}

int has_pipe(char **args, int *pipe_pos) {
  for (int i = 0; args[i]; i++) {
    if (strcmp(args[i], "|") == 0) {
      *pipe_pos = i;
      return 1;
    }
  }
  return 0;
}

void execute_piped(char **args, int pipe_pos) {
  args[pipe_pos] = NULL;

  int pipefd[2];
  if (pipe(pipefd) < 0) { perror("pipe"); return; }

  pid_t left = fork();
  if (left < 0) { perror("fork"); return; }

  if (left == 0) {
    close(pipefd[0]);
    dup2(pipefd[1], STDOUT_FILENO);
    close(pipefd[1]);
    execvp(args[0], args);
    perror(args[0]);
    _exit(127);
  }

  pid_t right = fork();
  if (right < 0) { perror("fork"); return; }

  if (right == 0) {
    close(pipefd[1]);
    dup2(pipefd[0], STDIN_FILENO);
    close(pipefd[0]);
    char **right_args = args + pipe_pos + 1;
    execvp(right_args[0], right_args);
    perror(right_args[0]);
    _exit(127);
  }

  close(pipefd[0]);
  close(pipefd[1]);
  waitpid(left, NULL, 0);
  waitpid(right, NULL, 0);
}

int has_redirect(char **args, int *pos, char **file, int *type) {
  for (int i = 0; args[i]; i++) {
    if (strcmp(args[i], ">") == 0) {
      *pos = i;
      *file = args[i + 1];
      *type = 1;
      args[i] = NULL;
      return 1;
    }
    if (strcmp(args[i], "<") == 0) {
      *pos = i;
      *file = args[i + 1];
      *type = 0;
      args[i] = NULL;
      return 1;
    }
  }
  return 0;
}

void execute(char **args, int bg) {
  int argc = 0;
  while (args[argc]) argc++;

  if (handle_builtin(args, argc)) return;

  int pipe_pos;
  if (has_pipe(args, &pipe_pos)) {
    execute_piped(args, pipe_pos);
    return;
  }

  char *redir_file;
  int redir_pos, redir_type;
  int has_redir = has_redirect(args, &redir_pos, &redir_file, &redir_type);

  pid_t pid = fork();
  if (pid < 0) { perror("fork"); return; }

  if (pid == 0) {
    if (has_redir) {
      int fd;
      if (redir_type == 1) {
        fd = open(redir_file, O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (fd < 0) { perror(redir_file); _exit(1); }
        dup2(fd, STDOUT_FILENO);
      } else {
        fd = open(redir_file, O_RDONLY);
        if (fd < 0) { perror(redir_file); _exit(1); }
        dup2(fd, STDIN_FILENO);
      }
      close(fd);
    }
    execvp(args[0], args);
    perror(args[0]);
    _exit(127);
  }

  if (!bg) {
    waitpid(pid, NULL, 0);
  } else {
    if (bg_count < MAX_BG_PROCS)
      bg_pids[bg_count++] = pid;
    printf("[%d] %d\n", bg_count, pid);
  }
}

void shell_loop(void) {
  char line[MAX_LINE];
  char *args[MAX_ARGS];

  while (1) {
    char cwd[1024];
    getcwd(cwd, sizeof(cwd));
    printf("mysh:%s$ ", cwd);
    fflush(stdout);

    if (fgets(line, sizeof(line), stdin) == NULL) {
      putchar('\n');
      break;
    }

    line[strcspn(line, "\n")] = '\0';

    char *trimmed = line;
    while (*trimmed == ' ' || *trimmed == '\t') trimmed++;
    if (*trimmed == '\0') continue;

    int bg = 0;
    int len = strlen(trimmed);
    if (len > 0 && trimmed[len - 1] == '&') {
      bg = 1;
      trimmed[len - 1] = '\0';
      char *end = trimmed + strlen(trimmed) - 1;
      while (end >= trimmed && (*end == ' ' || *end == '\t')) *end-- = '\0';
    }

    tokenize(trimmed, args);
    if (args[0] == NULL) continue;

    execute(args, bg);
  }
}

int main(void) {
  setup_signal_handlers();
  puts("Mini Shell -- type 'help' for commands");
  shell_loop();
  return 0;
}

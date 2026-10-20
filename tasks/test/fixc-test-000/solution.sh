cat > prog.c <<'EOF'
#include <stdio.h>
int main(){
  int x = 9 * 3;
  printf("%d\n", x);
  return 0;
}
EOF
cc prog.c -o prog
./prog > out.txt
cat out.txt

# Silly-Lang
A hobby functional programming language written in Python and C.

### Compiling:
Compilation currently only works on x86 based machines with nasm.
1. Make sure your program has the .silly extension.
2. `make main.o`
3. `make FILENAME.run`
4. `./FILENAME.run`

You may also quickly run a silly program with `python silly_run.py -c FILENAME.silly`

### Syntax and Design:
The last expression of a program is what is returned by the runtime system.
```
1 # returns 1
```
Also, comments are designated by the `#` character.

Silly-Lang is designed to mirror many familiar imperative programming patterns while being internally fully functional. The example program below demonstrates this.
```
f(x, y) =
  if   x > 10
  then x
  else y

x = 1
y = 2
z = f(x, y)

z + x + y # returns 5
```
The operator used to assign values to variables, and the operator used to check equality are combined syntactically (but separate semantically).
```
x = 1 # let binding
x = 1 # returns true
```
Values are immutable, but shadowing is allowed.
```
x = 1 # let binding
x = 2 # shadowing
x + 3 # returns 5
```
### Features and Plans:
Currently working features include booleans, ints, boolean operations (and, or, xor, not), integer operations (+, -, *, /), if expressions, let bindings, function definitions and calls.
Planned features include a static type checker (stlc), io, lambdas, cons lists, pattern matching, strings.
Possible future features include compiling to LLVM, [Nat](https://youtu.be/jFk1qpr1ytk?si=pEjIHgSNP2y34o3N), lazy evaluation, bootstrapping.

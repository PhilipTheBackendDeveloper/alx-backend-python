# ALX Backend Python

This repository contains different projects.  
The projects focus on advanced Python concepts, testing, and backend development practices.

---

# 📌 Topics Covered

This repository covers the following major topics:

1. **Unit Tests and Integration Tests**  
2. **Context Managers**  
3. **Decorators**  
4. **Generators**  
5. **Asynchronous Programming (async/await)**  

Each topic is explained separately below.

---

# 1️⃣ Unit Tests and Integration Tests

### 🔹 Introduction
- **Unit testing**: Test individual functions in isolation. External dependencies (e.g., databases, APIs) should be mocked.  
- **Integration testing**: Test how multiple components interact together, mocking only external requests.  

### 🔹 Why Important?
- Ensures reliability of functions.  
- Protects against regressions.  
- Encourages modular and maintainable code.  



# 2️⃣Context Managers
### 🔹 What They Are

A context manager handles setup and cleanup actions automatically (e.g., opening/closing a file).
They are commonly used with the with statement.

### 🔹 Example
```
with open("data.txt", "r") as f:
    content = f.read()
# file is automatically closed here
```
### 🔹 Custom Context Manager
```
class MyContext:
    def __enter__(self):
        print("Entering context")
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting context")

with MyContext():
    print("Inside block")
```
# 3️⃣ Decorators
🔹 What They Are

A decorator is a function that takes another function and extends its behavior without modifying it.

### 🔹 Example
```def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```
### 🔹 Usage in Repo

`@memoize in utils.py is a decorator that caches method results.`

# 4️⃣ Generators
🔹 What They Are

A generator is a function that yields values one at a time using yield, instead of returning them all at once.

### 🔹 Example
```
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

for num in count_up_to(5):
    print(num)
```
### 🔹 Why Useful?

Saves memory (lazy evaluation).

Perfect for streaming data or infinite sequences.

# 5️⃣ Asynchronous Programming
### 🔹 What It Is

Asynchronous programming allows multiple tasks to run concurrently without blocking each other.
Python uses async and await keywords for this.

### 🔹 Example
```
import asyncio

async def say_hello():
    await asyncio.sleep(1)
    print("Hello async!")

async def main():
    await asyncio.gather(say_hello(), say_hello())

asyncio.run(main())
```
### 🔹 Why Important?

Essential for backend services handling multiple requests.

Efficient handling of I/O-bound operations (APIs, databases).

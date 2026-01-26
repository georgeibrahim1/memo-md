# What is the time complexity of the following algorithm?
```python
def find_duplicates(arr):
    seen = set()
    duplicates = []
    for item in arr:
        if item in seen:
            duplicates.append(item)
        else:
            seen.add(item)
    return duplicates
```

<!--seperator-->

**Time Complexity: O(n)**

The algorithm iterates through the array once (n iterations). Set lookup and insertion operations are O(1) on average. Therefore, the overall time complexity is O(n) where n is the length of the array.

Space complexity is also O(n) in the worst case when all elements are unique.

---

# Which of the following are valid ways to create a virtual environment in Python?

<!--seperator-->

[*] `python -m venv myenv`
[ ] `pip install virtualenv myenv`
[*] `python -m virtualenv myenv`
[ ] `python --venv myenv`

---

# What is a closure in JavaScript?

<!--seperator-->

A closure is a function that has access to variables from its outer (enclosing) function's scope, even after the outer function has finished executing. Closures are created every time a function is created.

Example:
```javascript
function outer(x) {
    return function inner(y) {
        return x + y; // inner has access to x
    };
}
const add5 = outer(5);
console.log(add5(3)); // 8
```

---

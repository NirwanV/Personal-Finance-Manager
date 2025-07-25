<!DOCTYPE html>
<html>
<head>
    <title>Finance Manager</title>
</head>
<body>
    <h1>Personal Finance Manager</h1>
    <h2>Balance: ₹{{ balance }}</h2>

    <!-- Form to add new transactions -->
    <form action="/add" method="post">
        <label for="type">Transaction Type:</label>
        <select name="type" id="type" onchange="updateCategories()" required>
            <option value="Income">Income</option>
            <option value="Expense">Expense</option>
        </select>

        <label for="category">Category:</label>
        <select name="category" id="category" required></select>

        <label for="amount">Amount:</label>
        <input name="amount" placeholder="Amount" type="number" required>

        <label for="note">Note:</label>
        <input name="note" placeholder="Note">

        <label for="date">Date:</label>
        <input name="date" type="date" required>

        <button type="submit">Add</button>
    </form>

    <h3>Transaction History</h3>
    <ul>
        {% for t in transactions %}
            <li>[{{ t[5] }}] {{ t[1] }} - ₹{{ t[3] }} ({{ t[2] }}) : {{ t[4] }}</li>
        {% endfor %}
    </ul>

    <button onclick="window.location.href='/download-pdf'">Download Report (PDF)</button>

    <script>
        function updateCategories() {
            const type = document.getElementById('type').value;
            const categorySelect = document.getElementById('category');
            categorySelect.innerHTML = '';  // Clear options

            fetch('/categories.json')
                .then(response => response.json())
                .then(data => {
                    let options = type === 'Income' ? data.Income : data.Expense;

                    if (!options || options.length === 0) {
                        console.error("No categories found for", type);
                        return;
                    }

                    options.forEach(category => {
                        const option = document.createElement('option');
                        option.value = category;
                        option.textContent = category;
                        categorySelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching categories:', error));
        }

        // Call function when page loads
        window.onload = updateCategories;
    </script>
</body>
</html>

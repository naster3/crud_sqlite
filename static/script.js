
    function checkInputType() {
        var query = document.getElementById('query').value;
        var dateRegex = /^\d{4}-\d{2}-\d{2}$/;

        if (dateRegex.test(query)) {
            document.getElementById('query').type = 'date';
        } else {
            document.getElementById('query').type = 'text';
        }
    }


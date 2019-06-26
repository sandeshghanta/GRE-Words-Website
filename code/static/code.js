function init() {
    if (!document.getElementById("input-box")) {
        setTimeout(init, 500);
    } else {
        //        document.getElementById("input-box").addEventListener("input", shrink_container());
        init_autocomplete();
        document.getElementById("input-box").addEventListener("keyup", function(event) {
            event.preventDefault();
            var query = this.value;
            if (query.length > 0){
                shrink_container();
            }
            else{
                expand_container();
                clear_results();
            }
            if (event.keyCode === 13) {
                expand_container();
                document.getElementById("submit-button").click();
            }
        });
    }

}
init();

function init_autocomplete(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            autocomplete(document.getElementById("input-box"), data.words);
        }

    };
    xhttp.open("POST", "get_all_words", true);
    xhttp.send();
}

function search() {
    query = document.getElementById("input-box").value;
    query = query.replace(/\s/g, "");
    if (!query || query.length == 0) {
        document.getElementById("input-box").value = null;
        return;
    }
    clear_results();
    data = query_db(query);
}

function query_db(query) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            if (data['empty']){
                show_empty_result();
            }
            else{
                display_results(data['sentences'])
            }
        }
    };
    xhttp.open("POST", "search/"+query, true);
    xhttp.send();
}

function display_results(sentences){
    results = document.getElementById("results");
    results.style.display = "block";
    sentences.forEach(function(sentence){
        var result = document.createElement("div");
        result.className = "result";
        result.innerHTML = sentence;
        results.appendChild(result);
    });
}
function show_empty_result(){

}

function clear_results() {
    var results = document.getElementById("results");
    while (results.lastElementChild) {
        results.removeChild(results.lastElementChild);
    }
    results.style.display = "none";
}

function shrink_container() {
    var container = document.getElementById("container");
    container.style.paddingLeft = "30%";
    container.style.paddingRight = "30%";
}

function expand_container() {
    var container = document.getElementById("container");
    container.style.paddingLeft = "20%";
    container.style.paddingRight = "20%";
}

function autocomplete(inp, arr) {
    var currentFocus;
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(a);
        for (i = 0; i < arr.length; i++) {
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                b = document.createElement("DIV");
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                b.addEventListener("click", function(e) {
                    inp.value = this.getElementsByTagName("input")[0].value;
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            currentFocus++;
            addActive(x);
        } else if (e.keyCode == 38) { //up
            currentFocus--;
            addActive(x);
        } else if (e.keyCode == 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    document.addEventListener("click", function(e) {
        closeAllLists(e.target);
    });



}
const share = async () => {
    try {
        const location = window.location.href.slice(7); // Get the URL without the protocol
        // Remove the '?page' parameter if it exists
        const url = location.split('?')[0];
        await navigator.clipboard.writeText(url);
        const copyPopup = document.getElementById("copyPopup");
        copyPopup.classList.toggle("show");
    } catch (err) {
        alert("Failed to copy link");
    }
}

function goToSet(set_id) {
    document.location.href = `/view-set/${parseInt(set_id)}`;
}

function showDetails() {
    const detailsPopup = document.getElementById("detailsPopup");
    detailsPopup.classList.toggle("show");
}

function showOneCard() {
    document.querySelector("#all-cards-view").style.display = 'none';
    document.querySelector("#one-card-view").style.display = 'block';
    document.querySelector("#edit-view").style.display = 'none';
}

function showAllCards() {
    document.querySelector("#all-cards-view").style.display = 'block';
    document.querySelector("#one-card-view").style.display = 'none';
    document.querySelector("#edit-view").style.display = 'none';
}

function edit() {
    document.querySelector("#all-cards-view").style.display = 'none';
    document.querySelector("#one-card-view").style.display = 'none';
    document.querySelector("#edit-view").style.display = 'block';
}

function resetTestPage() {
    answer.value = "";
    prompt.innerHTML = "Enter the correct definition above.";
    prompt.style.display = "none";
    if (!nextbtn.classList.contains('disabled-link')) {
            nextbtn.classList.add('disabled-link');
        }
    nextbtn.classList.add('btn-light');
    nextbtn.classList.remove('btn-info');
}

document.addEventListener('DOMContentLoaded', () => {

    // index.html
    const indexSets = document.querySelectorAll(".existing-oneset-div");
    if (indexSets) {
        indexSets.forEach((set) => {
            set.addEventListener('click', function() {
                goToSet(set.id);
            })
        })
    }

    // add-cards-csv.html file processing
    const customFile = document.querySelector('#customFile');
    if (customFile) {
        customFile.addEventListener('change', function(event) {
            const input = event.target;
            const fileName = input.files[0].name;
            const label = input.nextElementSibling;
            label.innerHTML = fileName;
        })
    }

    // collection.html & user.html
    const sets = document.querySelectorAll(".set-div");
    if (sets) {
        sets.forEach((set) => {
            set.addEventListener('click', function() {
                goToSet(set.id);
            })
        })
    }

    // Add card functionality in create.html and set.html
    const nTermsInput = document.querySelector('#nTerms');
    const addCardsBtn = document.querySelector('.add-card-button');

    if (nTermsInput && addCardsBtn) {
        addCardsBtn.addEventListener('click', function(event) {
            event.preventDefault();
            const nTerms = parseInt(nTermsInput.value);
            const cardForm = document.createElement("div");
            cardForm.className = "card-form";
            cardForm.innerHTML = `
                <div class="form-group">
                    <input class="form-control" name="card_${nTerms}_term" placeholder="Term ${nTerms + 1}" type="text">
                </div>
                <div class="form-group">
                    <input class="form-control" name="card_${nTerms}_definition" placeholder="Definition" type="text">
                </div>
            `;
            nTermsInput.value = nTerms + 1;
            
            // Find the closest form element and then find the ".add-card-div" within it
            addCardsBtn.closest('form').querySelector(".add-card-div").appendChild(cardForm);
        });
    }

    // Delete button & functionality in set.html and study.html
    const modal = document.getElementById("deleteModal");
    const btn = document.getElementById("delete-btn");
    const span = document.getElementsByClassName("close")[0];
    
    if (btn && span) {
        
        btn.onclick = function(event) {
            event.preventDefault();
            modal.style.display = "block";
        }
        span.onclick = function() {
            modal.style.display = "none";
        }
    }
    
    const nobtn = document.querySelector(".no");
    
    if (nobtn) {
        nobtn.onclick = function(event) {
            event.preventDefault();
            modal.style.display = "none";
        }
    }

    if (modal) {
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    }

    // study.html
    const hintbtn = document.querySelector('#hint-btn');
    const hint = document.querySelector("#hint");
    const prompt = document.querySelector("#prompt");
    const answer = document.querySelector("#answer");
    const nextbtn = document.querySelector('.next-btn');

    if (hintbtn) {
        hintbtn.onclick = function() {
            answer.value = "";
            answer.placeholder = hint.value;
            prompt.innerHTML = "Enter the correct definition above."
            prompt.style.display = "block";
        }
    }

    if (answer && hint) {
        answer.addEventListener('change', function() { 
            if (answer.value === hint.value) {
                nextbtn.classList.remove('disabled-link');
                nextbtn.classList.remove('btn-light');
                nextbtn.classList.add('btn-info');
                nextbtn.addEventListener('click', resetTestPage);
                prompt.innerHTML = "Correct!";
                prompt.style.display = "block";
            } else {
                prompt.innerHTML = "Incorrect.";
                prompt.style.display = "block";
                if (!nextbtn.classList.contains('disabled-link')) {
                    nextbtn.classList.add('disabled-link');
                }
                nextbtn.classList.add('btn-light');
                nextbtn.classList.remove('btn-info');
                nextbtn.removeEventListener('click', resetTestPage);
            }
        })
    }

    // test.html
    const testAnswers = document.querySelectorAll(".test-answer");
    const finishbtn = document.querySelector('.finish-btn');

    if (testAnswers && finishbtn) {
        testAnswers.forEach((testAnswer) => {
            testAnswer.addEventListener('change', function() { 
                finishbtn.classList.remove('disabled-link');
                finishbtn.classList.remove('btn-light');
                finishbtn.classList.add('btn-info');
            })
        })
    }
})
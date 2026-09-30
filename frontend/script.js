
const API_URL = "http://127.0.0.1:8000/analyze";


async function analyzeCode() {

    const codeInput =
        document.getElementById("codeInput");

    const analyzeButton =
        document.getElementById("analyzeButton");

    const results =
        document.getElementById("results");


    const code = codeInput.value.trim();


    if (!code) {

        alert("Please enter some Java code.");

        return;
    }


    analyzeButton.disabled = true;

    analyzeButton.textContent = "Analyzing...";


    try {

        const response = await fetch(
            API_URL,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    code: code
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );
        }


        const data =
            await response.json();


        displayResults(data);


    } catch (error) {

        console.error(error);

        results.classList.remove("hidden");

        results.innerHTML = `
            <div class="error">
                <strong>Analysis failed.</strong>
                <br><br>
                Make sure the CodeSense FastAPI
                server is running on port 8000.
                <br><br>
                Error: ${error.message}
            </div>
        `;


    } finally {

        analyzeButton.disabled = false;

        analyzeButton.textContent =
            "Analyze Code";
    }
}


function displayResults(data) {

    const results =
        document.getElementById("results");


    results.classList.remove("hidden");


    document.getElementById("score").textContent =
        data.quality_score;


    document.getElementById("totalLines").textContent =
        data.metrics.total_lines;


    document.getElementById("classes").textContent =
        data.metrics.classes;


    document.getElementById("methods").textContent =
        data.metrics.methods;


    updateScoreMessage(
        data.quality_score
    );


    displayIssues(
        data.issues
    );


    results.scrollIntoView({
        behavior: "smooth"
    });
}


function updateScoreMessage(score) {

    const message =
        document.getElementById("scoreMessage");


    if (score >= 90) {

        message.textContent =
            "Your code has a strong quality profile.";

    } else if (score >= 70) {

        message.textContent =
            "Your code is reasonably structured, but some improvements are recommended.";

    } else {

        message.textContent =
            "Several improvements could make this code cleaner and easier to maintain.";
    }
}


function displayIssues(issues) {

    const container =
        document.getElementById(
            "issuesContainer"
        );


    if (!issues || issues.length === 0) {

        container.innerHTML = `
            <div class="no-issues">
                ✓ No code smells detected.
            </div>
        `;

        return;
    }


    container.innerHTML =
        issues.map(issue => {

            let extraDetails = "";


            if (issue.lines) {

                extraDetails +=
                    `<br>Lines: ${issue.lines}`;
            }


            if (issue.depth) {

                extraDetails +=
                    `<br>Depth: ${issue.depth}`;
            }


            return `
                <div class="issue-card">

                    <div class="issue-header">

                        <span class="issue-type">
                            ${issue.type}
                        </span>

                        <span class="issue-severity">
                            ${issue.severity}
                        </span>

                    </div>

                    <div class="issue-message">

                        ${issue.message}

                        ${extraDetails}

                    </div>

                    <div class="issue-suggestion">

                        💡 ${issue.suggestion}

                    </div>

                </div>
            `;

        }).join("");
}


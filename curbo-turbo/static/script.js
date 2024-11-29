var titnameval = 'Рекомендации'
function toggleSubcategories(id) {
    const subcategory = document.getElementById(id);
    if (subcategory.style.display === "block") {
        subcategory.style.display = "none";
    } else {
        subcategory.style.display = "block";
    }
}

function loadContent(section) {
    const contentArea = document.getElementById("main-content");

    switch (section) {
        case 'subcategory1-item1':
            contentArea.innerHTML = `
                <h2>Subcategory 1-1</h2>
                <p>This is content for Subcategory 1-1.</p>`;
            break;
        case 'subcategory1-item2':
            contentArea.innerHTML = `
                <h2>Subcategory 1-2</h2>
                <p>This is content for Subcategory 1-2.</p>`;
            break;
        // Add more cases as needed
        default:
            contentArea.innerHTML = `<h2>Welcome</h2><p>Select a category to view its content.</p>`;
    }
}

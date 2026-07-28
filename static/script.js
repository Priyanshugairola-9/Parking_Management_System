function submitForm(formId, url) {
    const form = document.getElementById(formId);
    fetch(url, {
        method: "POST",
        body: new FormData(form)
    })
    .then(res => res.text())
    .then(data => alert(data));
}

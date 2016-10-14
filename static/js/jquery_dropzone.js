// Get the template HTML and remove it from the doumenthe template HTML and remove it from the doument
var alert = false;
var previewNode = document.querySelector("#template");
previewNode.id = "";
var previewTemplate = previewNode.parentNode.innerHTML;
previewNode.parentNode.removeChild(previewNode);

var myDropzone = new Dropzone(document.body, { // Make the whole body a dropzone
    url: "/upload_file_action/", // Set the url
    maxFiles: 1,
    thumbnailWidth: 80,
    thumbnailHeight: 80,
    parallelUploads: 20,
    previewTemplate: previewTemplate,
    autoQueue: false, // Make sure the files aren't queued until manually added
    previewsContainer: "#previews", // Define the container to display the previews
    clickable: ".fileinput-button" // Define the element that should be used as click trigger to select files.
});

myDropzone.on("addedfile", function (file) {
    // Hookup the start button
    file.previewElement.querySelector(".start").onclick = function () { myDropzone.enqueueFile(file); };
});

// Update the total progress bar
myDropzone.on("totaluploadprogress", function (progress) {
    document.querySelector("#total-progress .progress-bar").style.width = progress + "%";
});

myDropzone.on("sending", function (file) {
    // Show the total progress bar when upload starts
    // document.querySelector("#total-progress").style.opacity = "1";
    // And disable the start button
    file.previewElement.querySelector(".start").setAttribute("disabled", "disabled");
});

// Hide the total progress bar when nothing's uploading anymore
myDropzone.on("queuecomplete", function (progress) {
    document.querySelector("#total-progress").style.opacity = "0";
    window.location = "/upload_metadata";
});

myDropzone.on("maxfilesexceeded", function (file) {
    if (!alert) {
        BootstrapDialog.show({
            title: 'Informação',
            message: 'Por enquanto só é possível enviar um arquivo por vez.',
            closable: true,
            closeByBackdrop: false,
            closeByKeyboard: false,
            buttons: [{
                label: 'Ok',
                action: function (dialogRef) {
                    dialogRef.close();
                }
            }]
        });
        alert = true;
    }
    this.removeFile(this.files[0]);
    this.removeFile(file);
    this.addFile(file);
});
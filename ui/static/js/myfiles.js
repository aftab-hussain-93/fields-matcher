const deleteFile = (fileId, userId) => {
    console.log("File to delete")
    console.log("AJAX request to delete from AWS and from Mongo. If parent file is being delete then delete all the versions of it as well.")
    // Use queue system to delete from AWS. Set status as deleted in Mongo.
    // Write a function to delete a file.
    // Page reload after deletion
}
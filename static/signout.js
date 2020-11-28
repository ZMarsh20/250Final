if (confirm("Are you sure you want to Sign Out?")){
    location.assign("\\logout");
} 
else {
    window.history.back();
}
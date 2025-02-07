function changeTab(vid) {
	vidTab = document.getElementById("vid-tab");
	vidForm = document.getElementById("vid-form");
	imgTab = document.getElementById("img-tab");
	imgForm = document.getElementById("img-form");
	if (vid) {
		vidTab.classList.add("bg-light", "text-dark");
		vidTab.classList.remove("text-light");
		vidForm.classList.remove("d-none");
		imgTab.classList.add("text-light");
		imgTab.classList.remove("bg-light", "text-dark");
		imgForm.classList.add("d-none");
	} else {
		imgTab.classList.add("bg-light", "text-dark");
		imgTab.classList.remove("text-light");
		imgForm.classList.remove("d-none");
		vidTab.classList.add("text-light");
		vidTab.classList.remove("bg-light", "text-dark");
		vidForm.classList.add("d-none");
	}
}

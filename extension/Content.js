const customThumbnail = "https://static.scientificamerican.com/sciam/cache/file/F766A67E-A8AA-4C90-A929C9AC67075D4B_source.jpg?w=1350"

// content.js

function replaceThumbnails() {
  document.querySelectorAll("img").forEach(img => {
    if (img.src.includes("ytimg.com")) {
      img.src = customThumbnail;
    }
  });
}

// Run initially and observe DOM changes for dynamic loading
replaceThumbnails();
const observer = new MutationObserver(replaceThumbnails);
observer.observe(document.body, { childList: true, subtree: true });

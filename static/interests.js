document.getElementById("interest_form").onsubmit = function (e) {
  e.preventDefault();

  fetch("/interests", {
    method: "POST",
    body: JSON.stringify({
      name: document.getElementById("name").value,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (jsonResponse) {
      console.log(jsonResponse);
      if (jsonResponse["success"] == true) {
        load_interests();
      } else {
        console.log("An Error Occurred!");
      }

      //window.location.reload(true);
    });
};

load_interests = function () {
  fetch("/interests", {
    method: "GET",
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (jsonResponse) {
      console.log(jsonResponse);
      document.getElementById("interests").innerHTML = ""
      for (let ind = 0; ind < jsonResponse["interests"].length; ind++) {
        const liItem = document.createElement("LI");
        liItem.className = "list-group-item";
        liItem.innerHTML = jsonResponse["interests"][ind]["name"];
        document.getElementById("interests").appendChild(liItem);
      }
    });
};

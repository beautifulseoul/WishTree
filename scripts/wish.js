// API


$(document).ready(function () {
show_wish();
});

function show_wish() {
$.ajax({
    type: "GET",
    url: "/wish",
    data: {},
    success: function (response) {
    alert(response["msg"]);
    },
});
}

function save_wish() {
$.ajax({
    type: "POST",
    url: "/wish",
    data: { wish_give: "소원 전송" },
    success: function (response) {
    alert(response["소원 전송됨!"]);
    window.location.reload();
    },
});
}

function done_wish(num) {
$.ajax({
    type: "POST",
    url: "/wish/done",
    data: { wish_give: "소원 성취" },
    success: function (response) {
    alert(response["소원 성취!"]);
    },
});
}




//친구 트리 놀러가기 버튼 누르면 다른 페이지로 이동하는 기능
function toOthers() {
  window.location.href = "sample.html";
}

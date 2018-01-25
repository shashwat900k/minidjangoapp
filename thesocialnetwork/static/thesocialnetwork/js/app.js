$(document).ready(function(){

  $('.search-button').on('click', searchUsers);
  $('.send-friend-request').on('click', sendFriendRequest);
  $('.accept-request').on('click', acceptRequest)


});

function searchUsers(){
  let input = $('.search-term').val()
  if (input!=''){
    window.location.replace('/search/'+input)
  }
}

function sendFriendRequest(){
  let input = $(this).children().text()
  window.location.replace('/send_request/'+input);
}

function acceptRequest(){
  let input = $(this).children().first().text()
  window.location.replace('/accept_request/'+input)
}

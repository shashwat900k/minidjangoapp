$(document).ready(function(){

  $('.search-button').on('click', searchUsers);
  $('.send-friend-request').on('click', sendFriendRequest);
  $('.accept-request').on('click', acceptRequest)
  $('.reject-request').on('click', rejectRequest)
  $('.like-post').on('click', likePost)
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
  let input =  $(this).children().text()
  window.location.replace('/accept_request/'+input);
}

function rejectRequest(){
  let input =  $(this).children().text()
  window.location.replace('/reject_request/'+input);
}

function likePost(){
  let input =  $(this).children().text()
  input = $.trim(input)
  window.location.replace('/user_reaction/'+input)
}

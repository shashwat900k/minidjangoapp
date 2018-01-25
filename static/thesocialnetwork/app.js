$(document).ready(function(){

  $('.search-button').on('click', searchUsers);

}

function searchUsers(){
  let input = $('.search-term').text()
  if (input!=''){
    window.location.replace('/search/'+input)
  }
}


$(document).ready(function(){
   console.log('web page is ready');
   $('#inference').click(async function(){
       console.log('button was clicked');
       const res_name = String($('#rname').val());
       const data = {
           res_name
       };
       console.log(data);

       // ajax asynchronously sends message
       const response = await $.ajax('/inference', {  // browser sends message to server
           data: JSON.stringify(data),
           method: 'post',
           contentType: 'application/json'
       });

       console.log('response', response);
       $('#risk_output').val(response.prediction);

   });
  
});

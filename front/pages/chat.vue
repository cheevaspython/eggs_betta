<template>
  <div>
    <h4>Hi - <span id="username"></span></h4>
    <textarea id="chat-log" cols="100" rows="20"></textarea><br>
    <input id="chat-message-input" type="text" size="100"><br>
    <input id="chat-message-submit" type="button" value="Send">
  </div>
</template>
  
<script>
export default {
  name: 'chat',
  components: {
    
  },
  data() {
    return {
      token: localStorage.getItem('access_token'),
      webSocket: null
    }
  },
  methods: {

  },
  computed: {
    
  },
  created() {
    console.log('connecting WebSocket')
    this.webSocket = new WebSocket(`ws://${window.location.host}/ws/chat/?token=${this.token}`)
  },
  beforeDestroy() {
    this.webSocket.close()
  }
}

// this.webSocket.onmessage = (event) => {
  // console.log(event)
  // const data = JSON.parse(event.data);
  // console.log('RealTime', data.data)
  // switch (data.action) {
  //   case "retrieve":
  //     console.log(data.data)
  //     document.getElementById('username').innerText = data.data.host.username
  //     for (let mess of data.data.messages) {
  //       console.log(mess.text)
  //     }
  //     break;
  //   case "create":
  //     console.log(data.action, data.data)
  //     break;
  //   default:
  //     break;
  // }
// }

// this.webSocket.onopen = function() {
//   this.webSocket.send(
//     JSON.stringify({
//       pk: room_pk,
//       action: "join_room",
//       request_id: request_id,
//     })
//   )

//   this.webSocket.send(
//     JSON.stringify({
//       pk: room_pk,
//       action: "retrieve",
//       request_id: request_id,
//     })
//   )

//   this.webSocket.send(
//     JSON.stringify({
//       pk: room_pk,
//       action: "subscribe_to_messages_in_room",
//       request_id: request_id,
//     })
//   )

//   this.webSocket.send(
//     JSON.stringify({
//       pk: room_pk,
//       action: "subscribe_instance",
//       request_id: request_id,
//     })
//   )
// }



// Это исходный код бедолаги)

// const room_pk = "{{ room.pk }}"
// const request_id = new Date().getTime()
// const token = ''
// console.log(room_pk)
// console.log(request_id)
// console.log("request", '{{request}}')
// const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/?token=${localStorage.getItem('Token')}`)

// chatSocket.onopen = function () {
//     chatSocket.send(
//         JSON.stringify({
//             pk: room_pk,
//             action: "join_room",
//             request_id: request_id,
//         })
//     );
//     chatSocket.send(
//         JSON.stringify({
//             pk: room_pk,
//             action: "retrieve",
//             request_id: request_id,
//         })
//     );
//     chatSocket.send(
//         JSON.stringify({
//             pk: room_pk,
//             action: "subscribe_to_messages_in_room",
//             request_id: request_id,
//         })
//     );
//     chatSocket.send(
//         JSON.stringify({
//             pk: room_pk,
//             action: "subscribe_instance",
//             request_id: request_id,
//         })
//     );
// };

// chatSocket.onmessage = function (e) {
//     const data = JSON.parse(e.data);
//     console.log('RealTime', data.data)
//     switch (data.action) {
//         case "retrieve":
//             console.log(data.data)
//             document.getElementById('username').innerText = data.data.host.username
//             for (let mess of data.data.messages) {
//                 console.log(mess.text)
//             }

//             //setRoom(old =>data.data);
//             //setMessages(old=>data.messages);
//             break;
//         case "create":
//             console.log(data.action, data.data)
//             //setMessages(old=>[...old, data])
//             break;
//         default:
//             break;
//     }
// };

// chatSocket.onclose = function (e) {
//     console.error('Chat socket closed unexpectedly');
// };

// $('#chat-message-input').focus();
// $('#chat-message-input').on('keyup', function (e) {
//     if (e.keyCode === 13) {  // enter, return
//         document.querySelector('#chat-message-submit').click();
//     }
// });
// $('#chat-message-submit').on('click', function (e) {
//     const message = $('#chat-message-input').val();
//     chatSocket.send(JSON.stringify({
//         message: message,
//         action: "create_message",
//         request_id: request_id,
//     }));
//     $('#chat-message-input').val('');
// });
</script>

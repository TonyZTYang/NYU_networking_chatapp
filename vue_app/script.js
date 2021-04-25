var app = new Vue({
    el: '#app',
    data: {
      loggedIn: false,
      loginAlert: "",
      myId: "",
      myRoom:"",
      activeUsers: [],
      loginInput: "",
      user_room_change: 0,
      messageChange: 0,
      messages: [],
      loop: false,
      messageInput: ""
    },
    methods: {
      login: function() {
        var self = this;
        axios.post("/login", {
          username: this.loginInput
        })
        .then(function(response) {
          if (response.data.status == 1) {
            console.log("post response returned");
            self.myId = self.loginInput;
            self.loginInput = "";
            self.loggedIn = true;
            self.myRoom = "Public";
            self.loop = true;
            self.getUserRoomChange();
            self.getMessageChange();
          } else {
            self.loginAlert = "Duplicated username, please try again."
          }
        });
      },
      logout: function() {
        var self = this;
        axios.post("/logout", {
          username: this.myId
        })
        .then(function(response) {
          if (response.data.status == 1) {
            console.log("user deleted");
            self.myId = "";
            self.myRoom = "";
            self.loggedIn = false;
            self.loop = false;
            self.user_room_change = 0;
            self.messageChange = 0;
            self.messages = [];
          }
        });
      },
      getUserRoomChange: function() {
        var self = this;
        axios.post("/getUserRoomChange", {
          user_room_change: this.user_room_change,
          username: this.myId
        })
        .then(function(response) {
          if (response.data.changed == 1) {
            self.user_room_change = response.data.server_urc;
            updatedUsers = [];
            for (var user in response.data.users) {
              if (user == self.myId) {
                if (self.myRoom != response.data.users[user]) {
                  self.myRoom = response.data.users[user];
                  self.messageChange = 0
                }
                
              } else {
                updatedUsers.push({
                  name: user,
                  roomNumber: response.data.users[user] 
                })
              }
            }
            self.activeUsers = updatedUsers;
          }
        });
        if (this.loop) {
          setTimeout(() => {this.getUserRoomChange()}, 500);
        }
      },
      makeUserRoomChange: function(username) {
        var self = this;
        axios.post("/makeUserRoomChange", {
          myName: this.myId,
          otherName: username
        })
        .then(function(response) {
          if (response.data.status == 1) {
            console.log("change success");
          } 
        })
      },
      getMessageChange: function() {
        var self = this;
        axios.post("/getMessageChange", {
          username: this.myId,
          messageChange: this.messageChange
        })
        .then(function(response) {
          if (response.data.changed == 1) {
            console.log("detect message change")
            console.log(response.data.messages)
            self.messageChange = response.data.messageChange;
            newMessages = [];
            for (var msg in response.data.messages) {
              console.log(msg)
              newMessages.push({
                time: response.data.messages[msg][0],
                name: response.data.messages[msg][1],
                content: response.data.messages[msg][2]
              })
            }

            // for (let i = 0; i < self.messageChange; i++) {
            //   newMessages.push({
            //     time: response.data.messages[i]["time"],
            //     name: response.data.messages[i]["name"],
            //     content: response.data.messages[i]["text"]
            //   })
            // }
            self.messages = newMessages;
            console.log(newMessages)
            console.log[self.messages]
            
          }
        });
        if (this.loop) {
          setTimeout(() => {this.getMessageChange()}, 500);
        }
      },
      sendMessage: function() {
        var self = this;
        axios.post("/sendMessage", {
          username: this.myId,
          message: this.messageInput
        })
        .then(function(response) {
          self.messageInput = "";
          if (response.data.status == 1) {
            console.log("message sent");
          }
        })
      }
    }
  })
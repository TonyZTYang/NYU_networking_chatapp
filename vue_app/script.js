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
      loop: false
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
                myRoom = response.data.users[user];
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
        
      }
    }
  })
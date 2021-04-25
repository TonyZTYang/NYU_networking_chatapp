var app = new Vue({
    el: '#app',
    data: {
      loggedIn: false,
      loginAlert: "",
      myId: "",
      myRoom:"",
      activeUsers: [],
      loginInput: ""
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
          }
        })
      }
    }
  })
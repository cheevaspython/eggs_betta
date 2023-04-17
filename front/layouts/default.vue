<template>
  <div>
    <header class="header">
      <nav
        class="navbar header has-shadow has-text-weight-medium"
        role="navigation"
        aria-label="main navigation"
      >
        <div v-for="(item, key) of routes" :key="key" class="navbar-brand" style="align-items: center;" v-show="checkPermission(item.title)">

          <nuxt-link
            class="navbar-item link"
            @click="update"
            :to="item.to"
            :key="key"
            exact>
            {{ item.title }}
            <b-icon
              v-if="item.icon"
              :icon="item.icon"/>
          </nuxt-link>
        </div>
      </nav>
      <div class="user-info">
        <div class="user-card">
          <!-- @click="$router.push('/chat')" -->
          <b-icon
            icon="account"
            size="is-small"
            type="is-success"
            style="padding-top: 5px; margin-right: 5px;"/>
          {{ username }}
        </div>

        <section class="notif-btn" v-bind:style="{ 'background-color': getColor(notifications), 'color': getFontColor() }" @click="isCardModalActive = !isCardModalActive">
          <!-- <div class="flexbox flexbox__row" style="border-radius: 20px; cursor: pointer; justify-content: space-around;"> -->
            <b-icon icon="bell-outline" style="margin: 0 5px"/>
            <div class="newNotifications" v-show="newNotifications">{{ newNotifications }}</div>
          <!-- </div> -->
          <transition name="fade">
            <div v-if="isCardModalActive" style="position: absolute; left: 0; top: 0; z-index: 900; width: 100%; height: 100%; background-color: 0; cursor: default">
              <div class="notifications-window">
                <div class="notif-title">Уведомления</div>
                <div v-if="notifications.length == 0" class="no-notifications">Уведомлений нет</div>
                <ul style="height: 100%; width: 100%; overflow-y: scroll; padding: 0 10px; padding-top: 5px">
                  <li class="user-notifications" v-for="notif in notifications" :key="notif.id" @click="readMessage(notif)"
                    v-bind:style="{ 'border-color': getNotificationColor(notif.not_read), 'background-color': backgroundColor(notif.not_read) }"
                    v-bind:class="{ 'new': checkNewNotif(notif.not_read) }">
                    {{ notif.message }}
                  </li>
                </ul>
              </div>
            </div>
          </transition>
        </section>

        <b-button class="log-out-btn" @click="logOut()">
          <b-icon style="margin-top: 2px" icon="logout"/>
        </b-button>
      </div>

    </header>

    <section class="content">
      <Sidebar/>
      <div class="main text has-shadow">
        <nuxt/>
      </div>
    </section>
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";

export default {
  name: 'DefaultLayout',
  components: {
    Sidebar
  },
  data() {
    return {
      isCardModalActive: false,
      routes: [
        {
          title: '',
          icon: 'egg-outline',
          to: {name: 'index'}
        },
        {
          title: 'Продавцы',
          to: {name: 'sellers'}
        },
        {
          title: 'Покупатели',
          to: {name: 'buyers'}
        },
        {
          title: 'Логистика',
          to: {name: 'logistic'}
        },
        // {
        //   title: 'Документы',
        //   to: {name: 'documents'}
        // },
        {
          title: 'Статистика',
          to: {name: 'statistics'}
        },
      ],
      taskInterval: null,
      refreshInterval: null
    }
  },
  methods: {
    checkNewNotif(bool) {
      if (bool) {
        return true
      }
      else {
        return false
      }
    },
    backgroundColor(bool) {
      if (bool) {
        return '#fff'
        return '#ffe8e880'
      }
      else {
        return '#fff'
      }
    },
    getFontColor() {
      if (this.newNotifications > 0) {
        return '#fff'
      }
    },
    checkPermission(title) {
      const userRole = localStorage.getItem('userRole')
      if (title != 'Статистика') {
        return true
      }
      else if (title == 'Статистика' && userRole != '4') {
        return true
      }
      else {
        return false
      }
    },
    logOut: function() {
      this.$store.dispatch('authorization/logOut')
    },
    getColor(notifications) {
      let color = '#fff'
      notifications.forEach(n => {
        if (n.not_read === true) {
          color = '#ff1100cc'
        }
      })
      return color
    },
    async onItemClick(task) {
      switch(task.status) {
        case 1:
          await this.$store.dispatch('eggs/setCurrentCalculate', task)
          this.$router.push('/Calculate')
          break
        case 2:
          await this.$store.dispatch('eggs/setCurrentConfCalculate', task)
          this.$router.push('/ConfirmedCalculate')
          break
        case 3:
          await this.$store.dispatch('eggs/setCurrentDeal', task)
          this.$router.push('/Deal')
          break
        case "Покупатель":
          this.$router.push('/statisticFromMessage')
          break
      }
    },
    async getNotifications() {
      await this.$store.dispatch('user/getUserNotifications')
    },
    async getLogists() {
      await this.$store.dispatch('ca/getLogists')
    },
    async readMessage(notif) {
      if (notif.not_read) {
        await this.$store.dispatch('user/readNotification', notif.id)
        await this.$store.dispatch('user/getUserNotifications')
      }
      const task = await this.getTaskFromNotif(notif)
      this.onItemClick(task)
    },
    async getTaskFromNotif(notif) {
        if (notif.current_base_deal) {
          const task = await this.$store.dispatch('eggs/getModel', notif.current_base_deal)
          return task
        }
        else if (notif.current_buyer) {
          const buyer = await this.$store.dispatch('ca/getBuyerFromMessage', notif.current_buyer)
          return buyer
        }
    },
    getNotificationColor(not_read) {
      if (not_read) {
        return '#b7b7b7'
        return '#ff11001e'
      }
      else {
        return '#b7b7b7'
        return '#b3b3b3'
      }
    },
    async refreshUpdate() {
      await this.$store.dispatch('authorization/refreshToken')
    },
    async intervalUpdateNotifications() {
      setInterval(this.getNotifications, 60000)
      setInterval(this.refreshUpdate, 15000000)
      // setInterval(this.consoleClearing, 500)
    },
    async update() {
      await this.$store.dispatch('user/getUserNotifications')
      await this.$store.dispatch('bid/getOwnerTasks')
    },
    consoleClearing() {
      console.clear()
    }
  },
  async created() {
    this.getNotifications()
    this.intervalUpdateNotifications()
  },
  computed: {
    username() {
      return localStorage.getItem('username')
    },
    notifications() {
      return this.$store.state.user.notifications
    },
    newNotifications() {
      let newNotif = 0
      for (let notif of this.$store.state.user.notifications) {
        if (notif.not_read) {newNotif += 1}
      }
      return newNotif
    }
  }
}
</script>

<style lang="scss" scoped>
@media (min-width: 1600px) {
  .main {
    font-size: 18px;
  }
}

@media (min-width: 1200px) and (max-width: 1599px) {
  .main {
    font-size: 15px;
  }
}

.flexbox {
  display: flex;

  &__column {
    flex-direction: column;
    flex-flow: column;
  }
  &__row {
    flex-direction: row;
    flex-flow: row;
    display: inline-flex;
  }
  &__start {
    justify-content: flex-start;
  }
  &__center {
    justify-content: center;
  }
  &__end {
    justify-content: flex-end;
  }
  &__space-between{
    justify-content: space-between;
  }
}

div {
  font-family: 'Montserrat';
}

.new:before {
  content: 'Новое';
  color: #fff;
  background-color: #ff1100cc;
  border-radius: 10px;
  padding: 2px 5px;
  margin-right: 5px;
}

.link {
  font-family: 'Alkatra';
  // font-family: 'Josefin Sans';
  // font-family: 'Bebas Neue';
  font-size: calc(10px + 0.7vw);
  background-color: #fff;
  border-bottom: solid 2px #ebebeb;
  padding: 0 15px;
  min-width: 60px;
  height: 40px;
  justify-content: center;
  border-radius: 15px;
  margin-right: 5px;

  &:hover {
    border-color: #1e9bc8d0;
  }
}

.header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  padding: 0 20px;
}

.content {
  padding: 10px;
  display: grid;
  gap: 10px;
  grid-template-columns:  minmax(auto, 300px) 1fr;
  min-height: 50vh;
}

.user-info {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.main {
  font-family: 'Montserrat';
  width: 83vw;
  min-height: 91vh;
  background: #ffffff;
  border: 1px solid #f5f5f5;
  border-radius: 10px;
  padding: 10px;
}

.nuxt-link-active {
  color: rgb(61, 43, 226);
  border-bottom: 2px solid rgb(61, 43, 226);
  color: #1e6ac8e8;
  border-bottom: solid 2px #1e6ac8e8;
  background-color: #fff;
}

.title {
  text-align: center;
  font-size: 24px;
}

.notifications {
  padding: 0px 10px;
  cursor: pointer;
  border: solid #f5f5f5;
  text-align: center;
  border-radius: 10px;
  margin-bottom: 10px;
}

.newNotifications {
  // border: 2px solid #ebebeb;
  // border-radius: 20px;
  padding-right: 6px;
}

.notification-title {
  height: 100%;
  width: 100%;
}

.notif-btn {
  display: flex;
  justify-content: space-around;
  align-items: center;
  border: 1px solid hsl(0deg, 0%, 86%);
  border-radius: 10px;
  min-width: 40px;
  height: 40px;
  cursor: pointer;

  &:hover {
    border-color: #b5b5b5;
  }
}

.notifications-window {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: absolute;
  top: 64px;
  right: 20px;
  z-index: 1000;
  width: 500px;
  min-height: 100px;
  max-height: 90vh;
  padding-bottom: 5px;
  color: hsl(0deg, 0%, 29%);
  border: solid 3px #b7b7b7;
  border-radius: 15px;
  background-color: #f0f0f0;
  cursor: default;
}

.no-notifications {
  color: #7b7b7b;
  font-size: 20px;
  margin-bottom: 10px;
}

.notif-title {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  background-color: #fff;
  border-bottom: solid 2px #b7b7b7;
  border-radius: 15px;
  height: 40px;
  width: 100%;
  margin-bottom: 5px;
}

.user-notifications {
  width: 470px;
  padding: 10px;
  margin-bottom: 5px;
  background-color: #fff;
  border-bottom: solid 2px #ebebeb;
  border-radius: 10px;
  cursor: pointer;

  &:hover {
    outline: solid 2px #939393;
  }
}

// .fade-enter-active, .fade-leave-active {
//   transition: opacity .35s;
// }
// .fade-enter, .fade-leave-to {
//   opacity: 0;
// }

.fade-enter-active {
  transition: all .4s ease;
}
.fade-leave-active {
  transition: all .4s ease;
}
.fade-enter, .fade-leave-to {
  transform: translateX(400px);
  opacity: 0;
}

.user-card {
  display: flex;
  align-items: center;
  justify-content: center;
  border: solid hsl(0deg, 0%, 86%) 1px;
  padding: 0px 10px;
  border-radius: 10px;
  height: 40px;
}

.log-out-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  padding: 0;
}
</style>

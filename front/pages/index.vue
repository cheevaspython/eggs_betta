<template>
  <section class="section" style="padding: 0px">
    <div class="flexbox">
      <div v-if="hideFromLogic()" class="apps-button apps-button__apps" v-bind:class="{ active: showApps }" @click="appsClick">
        Заявки
      </div>
      <div v-show="hideFromLogic()" class="apps-button apps-button__calcs" v-bind:class="{ active: showCalcs }" @click="calcsClick">
        Просчеты
      </div>
      <div class="apps-button apps-button__conf-calcs" v-bind:class="{ active: showConfCalcs }" @click="confCalcsClick">
        Подтв. просчеты
      </div>
      <div class="apps-button apps-button__deals" v-bind:class="{ active: showDeals }" @click="dealsClick">
        Сделки
      </div>
    </div>
    <div class="tasks">
      <apps v-if="showApps"/>
      <calcs v-if="showCalcs"/>
      <confCalcs v-if="showConfCalcs"/>
      <deals v-if="showDeals"/>
    </div>
  </section>
</template>

<script>
export default {
  name: 'IndexPage',
  components: {
    apps: () => import('@/pages/apps'),
    calcs: () => import('@/pages/calculates'),
    confCalcs: () => import('@/pages/confirmedCalculates'),
    deals: () => import('@/pages/deals')
  },
  data() {
    return {
      showApps: false,
      showCalcs: false,
      showConfCalcs: false,
      showDeals: false,
      currentUserRole: localStorage.getItem('userRole')
    }
  },
  created() {
    if (this.currentUserRole == '4') {
      this.showConfCalcs = true
    }
    else {
      this.showApps = true
    }
  },
  methods: {
    hideFromLogic() {
      if (this.currentUserRole == '4') {
        return false
      }
      else {
        return true
      }
    },
    appsClick() {
      this.showCalcs = false
      this.showConfCalcs = false
      this.showDeals = false
      this.showApps = true
    },
    calcsClick() {
      this.showConfCalcs = false
      this.showDeals = false
      this.showApps = false
      this.showCalcs = true
    },
    confCalcsClick() {
      this.showDeals = false
      this.showApps = false
      this.showCalcs = false
      this.showConfCalcs = true
    },
    dealsClick() {
      this.showApps = false
      this.showCalcs = false
      this.showConfCalcs = false
      this.showDeals = true
    },
    navigate(rout) {
      this.$router.push(rout)
    },
    async onItemClick(task) {
      if (task) {
        switch(task.title) {
          case "Заявка от продавца":
            await this.$store.dispatch('eggs/setCurrentAppFromSeller', task)
            this.$router.push('/AppFromSeller')
            break
          case "Заявка от покупателя":
            await this.$store.dispatch('eggs/setCurrentAppFromBuyer', task)
            this.$router.push('/AppFromBuyer')
            break
          case "Просчет":
            await this.$store.dispatch('eggs/setCurrentCalculate', task)
            this.$router.push('/Calculate')
            break
          case "Подтвержденный просчет":
            await this.$store.dispatch('eggs/setCurrentConfCalculate', task)
            this.$router.push('/ConfirmedCalculate')
            break
          case "Сделка":
            await this.$store.dispatch('eggs/setCurrentDeal', task)
            this.$router.push('/Deal')
            break
        }
      }
    },
    getColor(task) {
      switch(task.title) {
        case "Заявка от продавца":
          return '#00a2ff15'
        case "Заявка от покупателя":
          return '#48ff0015'
        case "Просчет":
          return '#ffee0015'
        case "Подтвержденный просчет":
          return '#ff7b0015'
        case "Сделка":
          return '#ff110015'
      }
    },
    async getTaskFromNotif(notif) {
      const token = localStorage.getItem('access_token')
        if (notif.current_deal) {
          const deal = await this.$axios.get(`eggs/deal/${notif.current_deal}/`, {headers: {Authorization: `Bearer ${token}`}})
          deal.data.title = "Сделка"
          return deal.data
        }
        else if (notif.current_calculate) {
          const calculate = await this.$axios.get(`eggs/calculate/${notif.current_calculate}/`, {headers: {Authorization: `Bearer ${token}`}})
          calculate.data.title = "Просчет"
          return calculate.data
        }
        else if (notif.current_conf_calculate) {
          const confCalculate = await this.$axios.get(`eggs/confirmed_calculate/${notif.current_conf_calculate}/`, {headers: {Authorization: `Bearer ${token}`}})
          confCalculate.data.title = "Подтвержденный просчет"
          return confCalculate.data
        }
    },
    async readMessage(notif) {
      if (notif.not_read) {
        await this.$store.dispatch('user/readNotification', notif.id)
        await this.$store.dispatch('user/getUserNotifications')
      }

      const task = await this.getTaskFromNotif(notif)
      this.onItemClick(task)
    },
    getNotificationColor(not_read) {
      if (not_read) {
        return '#ff11001e'
      }
      else {
        return '#f5f5f5'
      }
    },
  },
  computed: {
    username() {
      return localStorage.getItem('username')
    },
    userRole() {
      return localStorage.getItem('userRole')
    },
    ownerTasks() {
      return this.$store.state.bid.ownerTasks
    },
    ownerNotifications() {
      return this.$store.state.user.notifications
    }
  }
}
</script>

<style lang="scss" scoped>
.title {
  font-size: 3vw;
  margin: 20px auto;
  text-align: center;
  width: 300px;
  border: solid #f5f5f5;
  border-radius: 10px;
  background-color: #f5f5f5;
  text-align: center;
}

.bar {
  border: 1px solid #f5f5f5;
  padding: 5px;
  margin: 10px 0;
  margin-left: auto;
  margin-right: auto;
  width: 60vw;
  border-radius: 5px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;

  &__title {
    font-size: 1.5vw;
    padding: 5px 20px;
    width: 100%;
    background-color: #f3f3f3;
    border-bottom: 1px solid #f5f5f5;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
  }
  &__item {
    width: 55vw;
    text-align: center;
    font-size: 14px;
    padding: 8px;
    border-bottom: 1px solid #f5f5f5;
    cursor: pointer;
    &:hover {
      background-color: #ffee0034;
    }
  }
}

.tasks {
  border: 2px solid #ebebeb;
  border-radius: 0 10px 10px 10px;
  padding-bottom: 10px;
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

.apps-button {
  display: flex;
  width: 250px;
  min-height: 35px;
  align-items: center;
  justify-content: center;
  text-align: center;
  border: solid #ebebeb 2px;
  border-bottom: 0;
  border-radius: 10px 10px 0 0;
  background-color: #ebebeb;
  cursor: pointer;
  margin-right: 5px;
  position: relative;
  
  &__apps {
    &:hover {
      border-color: #41e33882;
      background-color: #41e3382a;
    }
  }
  &__calcs {
    &:hover {
      border-color: #ffee0074;
      background-color: #ffee0015;
    }
  }
  &__conf-calcs {
    &:hover {
      border-color: #ff7b0074;
      background-color: #ff7b0015;
    }
  }
  &__deals {
    &:hover {
      border-color: #ff110061;
      background-color: #ff110015;
    }
  }
}

.active {
  background-color: #fff;
}

.active:after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  right: 0;
  height: 4px;
  background-color: #fff;
}
</style>

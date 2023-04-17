<template>
  <aside class="sidebar has-shadow ">
    <div v-if="ownerTasks" class="container is-fullwidth">
      <div class="sidebar__title">Мои заявки</div>
      <div v-for="task in ownerTasks" :key="ownerTasks[task]" class="sidebar__item" @click="onItemClick(task)">
        <div class="sidebar__row has-text-weight-medium" v-bind:style="{ 'background-color': getColor(task) }">
          {{ task.title }} №{{task.id}}
        </div>
      </div>
    </div>
  </aside>
</template>

<script>
export default {
  name: "Sidebar",
  data() {
    return {
      selectedOptions: []
    }
  },
  methods: {
    async onItemClick(task) {
      switch(task.title) {
        case "Заявка от продавца":
          const appSeller = await this.$store.dispatch('eggs/getSellerApp', task.id)
          await this.$store.dispatch('eggs/setCurrentAppFromSeller', appSeller)
          this.$router.push('/AppFromSeller')
          break
        case "Заявка от покупателя":
          const appBuyer = await this.$store.dispatch('eggs/getBuyerApp', task.id)
          await this.$store.dispatch('eggs/setCurrentAppFromBuyer', appBuyer)
          this.$router.push('/AppFromBuyer')
          break
        case "Просчет":
          const calculate = await this.$store.dispatch('eggs/getModel', task.id)
          await this.$store.dispatch('eggs/setCurrentCalculate', calculate)
          this.$router.push('/Calculate')
          break
        case "Подтвержденный просчет":
          const confCalculate = await this.$store.dispatch('eggs/getModel', task.id)
          await this.$store.dispatch('eggs/setCurrentConfCalculate', confCalculate)
          this.$router.push('/ConfirmedCalculate')
          break
        case "Сделка":
          const deal = await this.$store.dispatch('eggs/getModel', task.id)
          await this.$store.dispatch('eggs/setCurrentDeal', deal)
          this.$router.push('/Deal')
          break
      }
    },
    async getActiveTasks() {
      await this.updateActiveTasks()
      this.intervalUpdateTasks()
    },
    async updateActiveTasks(){
      await this.$store.dispatch('bid/getOwnerTasks')
    },
    async intervalUpdateTasks() {
      setInterval(this.updateActiveTasks, 60000)
    },
    getColor(task) {
      switch(task.title) {
        case "Заявка от продавца":
          return '#099cf115'
        case "Заявка от покупателя":
          return '#4ce21115'
        case "Просчет":
          return '#d4c60015'
        case "Подтвержденный просчет":
          return '#ff7b0015'
        case "Сделка":
          return '#ff110015'
      }
    },
  },
  async created() {
    this.getActiveTasks()
  },
  computed: {
    appsFromBuyer() {
      return this.$store.state.bid.appsFromBuyer
    },
    appsFromSeller() {
      return this.$store.state.bid.appsFromSeller
    },
    calculates() {
      return this.$store.state.bid.calculates
    },
    confCalculates() {
      return this.$store.state.bid.confCalculates
    },
    deals() {
      return this.$store.state.bid.deals
    },
    ownerTasks() {
      return this.$store.state.bid.ownerTasks
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebar {
  width: 15.5vw;
  border: 1px solid #f5f5f5;
  padding: 5px;
  border-radius: 10px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;

  &__title {
    padding: 5px 20px;
    width: 100%;
    background-color: #f3f3f3;
    border-radius: 10px;
    border-bottom: 1px solid #f5f5f5;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
  }

  &__item{
    text-align: center;
    margin: 5px 1px;
    border-radius: 10px;
    cursor: pointer;

    &:hover {
      background-color: #f5f5f5;
    }
  }

  &__row {
    border-radius: 10px;
  }
}

@media (min-width: 1600px) {
  .sidebar__item {
    font-size: 15px;
  }
}

@media (min-width: 1200px) and (max-width: 1599px) {
  .sidebar__item {
    font-size: 13px;
  }
}
.container{
  width: 100%;
}
</style>

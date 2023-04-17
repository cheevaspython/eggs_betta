<template>
  <div class="card-width">
    <Statistic :trader-data="buyerFromMessage" :both="true" :cash="false" />
  </div>
</template>

<script>
export default {
  name: 'statisticFromMessage',
  components: {
    Statistic: () => import("@/components/cards/Statistic")
  },
  computed: {
    buyerFromMessage() {
      return this.$store.state.ca.buyerFromMessage
    }
  },
  created() {
    if (!this.buyerFromMessage) {
      this.$router.push('/')
    }
  }
}
</script>

<style lang="scss" scoped>
@media (min-width: 1600px) {
  .card-width {
    width: 870px;
  }
}

@media (min-width: 1200px) and (max-width: 1599px) {
  .card-width {
    width: 650px;
  }
}
</style>
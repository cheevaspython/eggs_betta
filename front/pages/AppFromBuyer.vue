<template>
  <appFromBuyer :appFromBuyer="currentAppFromBuyer" />
</template>

<script>
export default {
  name: 'AppFromBuyerPage',
  components: {
    appFromBuyer: () => import("@/components/tasks/appFromBuyer")
  },
  computed: {
    currentAppFromBuyer() {
      return this.$store.state.eggs.currentAppFromBuyer
    }
  },
  created() {
    if (!this.currentAppFromBuyer) {
      this.$router.push('/')
    }
  }
}
</script>
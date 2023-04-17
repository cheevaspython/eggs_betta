<template>
  <appFromSeller :appFromSeller="currentAppFromSeller" />
</template>

<script>
export default {
  name: 'AppFromSellerPage',
  components: {
    appFromSeller: () => import("@/components/tasks/appFromSeller")
  },
  computed: {
    currentAppFromSeller() {
      return this.$store.state.eggs.currentAppFromSeller
    }
  },
  created() {
    if (!this.currentAppFromSeller) {
      this.$router.push('/')
    }
  }
}
</script>

<template>
  <div>
    <deal />
  </div>
</template>
  
<script>
export default {
  name: 'DealPage',
  components: {
    deal: () => import('@/components/tasks/deal')
  },
  data() {
    return {

    }
  },
  computed: {
    currentDeal() {
      return this.$store.state.eggs.currentDeal
    }
  },
  created() {
    if (!this.currentDeal) {
      this.$router.push('/')
    }
  }
}
</script>

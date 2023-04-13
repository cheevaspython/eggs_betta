<template>
  <div class="container buyers">
    <ul class="buyers-list">
      <li v-for="buyer in buyers" @click="onBuyersClick(buyer)" class="buyers-list__item">
        ИНН: <strong>{{ buyer.inn }}</strong>
        {{ buyer.name }}
      </li>
    </ul>
    <Card :trader-data="activeBuyer"/>
  </div>
</template>

<script>
export default {
  name: "buyers",
  data() {
    return {
      buyers: [],
      activeBuyer: null,
    }
  },
  // middleware: 'auth',
  async created() {
    this.buyers = await this.$store.dispatch('ca/getBuyers')
  },
  methods: {
    onBuyersClick(buyer) {
      console.log('b', buyer)
      this.activeBuyer = buyer
    }
  },
}
</script>

<style lang="scss" scoped>
.buyers {
  display: grid;
  grid-template-columns: 1fr 1fr;
  margin-left: 0;
}

.buyers-list {
  &__item {
    cursor: pointer;
    padding: 5px;
    border-bottom: 1px solid #f5f5f5;

    &:hover {
      background-color: #f5f5f5;
    }
  }

}
</style>

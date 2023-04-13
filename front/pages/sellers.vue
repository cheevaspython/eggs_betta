<template>
  <div class="container sellers">
    <ul class="sellers-list">
      <li v-for="seller in sellers" @click="onSellerClick(seller)" class="sellers-list__item">
        ИНН: <strong>{{ seller.inn }}</strong>
        {{ seller.name }}
      </li>
    </ul>
    <Card :trader-data="activeSeller"/>
  </div>
</template>

<script>
import Card from "@/components/Card";

export default {
  name: "sellers",
  components: {
    Card,
  },
  data() {
    return {
      activeTasks: {},
      sellers: [],
      activeSeller: null,
    }
  },
  methods: {
    onSellerClick(seller) {
      console.log(seller)
      this.activeSeller = seller
    }
  },
  async created() {
    // this.activeTasks = await this.$store.dispatch('bid/getActiveTasks')
    // this.sellers = this.activeTasks?.application_seller
    this.sellers = await this.$store.dispatch('ca/getSellers')
  }
}
</script>

<style lang="scss" scoped>
.sellers {
  display: grid;
  grid-template-columns: 1fr 1fr;
  margin-left: 0;
}

.sellers-list {
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

<template>
  <div class="flexbox flexbox__row">
    <div class="flexbox__row">
      <div class="flexbox_column">
        <div class="list-title">Сделки
          <b-button class="refresh-button" label="Обновить" type="is-warning" icon-left="refresh" @click="updateDeals" />
        </div>
        <ul class="deals">
          <li class="list-item flexbox flexbox__column" v-for="deal in deals" :key="deal.id" @click="setCurrentDeal(deal)"
            v-bind:style="{'border-color': getSelectedBorderColor(deal)}">
            <div  class="flexbox__row flexbox__space-between" style="margin-right: 0.15vw">
              <div class="flexbox__row" style="width: 45%">
                <div class="seller">{{ deal.seller_name }}</div>
                <div class="dates">{{ deal.delivery_date_from_seller }}</div>
              </div>
              <div style="align-self: center">№{{ deal.id }}</div>
              <div class="flexbox__row" style="width: 45%; justify-content: flex-end">
                <div class="dates">{{ deal.delivery_date_to_buyer }}</div>
                <div class="buyer">{{ deal.buyer_name }}</div>
              </div>
            </div>
            <div class="flexbox__row flexbox__center">
              <div>{{ status(deal) }}</div>
            </div>
            <div class="flexbox__row flexbox__space-between" style="width: 100%">
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(deal.cB), 
                'border-color': getBorderColor(deal.cB)}">
                <span v-show="deal.cB">CB: {{ deal.cB }} </span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(deal.c0), 
                'border-color': getBorderColor(deal.c0)}">
                <span v-show="deal.c0">C0: {{ deal.c0 }} </span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(deal.c1), 
                'border-color': getBorderColor(deal.c1)}">
                <span v-show="deal.c1">C1: {{ deal.c1 }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(deal.c2), 
               'border-color': getBorderColor(deal.c2)}">
                <span v-show="deal.c2">C2: {{ deal.c2 }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(deal.c3), 
                'border-color': getBorderColor(deal.c3)}">
                <span v-show="deal.c3">C3: {{ deal.c3 }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(deal.dirt), 
                'border-color': getBorderColor(deal.dirt)}">
                <span v-show="deal.dirt">Грязь: {{ deal.dirt }}</span>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div class="flexbox__row flexbox__space-between" style="width: 40vw">
      <transition name="fade">
        <div class="component" v-show="showDeal">
          <deal @toggle-card="updateDeals" v-if="currentDeal" />
        </div>
      </transition>
    </div>
  </div>
</template>
  
<script>
export default {
  name: "deals",
  components: {
    deal: () => import("@/components/tasks/deal")
  },
  data() {
    return {
      showDeal: false
    }
  },
  // middleware: 'auth',
  methods: {
    getBackgroundColor(eggs) {
      if (eggs) {
        return '#41e3382a'
      }
      else {
        return '#fff'
      }
    },
    getBorderColor(eggs) {
      if (eggs) {
        return '#cbcbcb'
      }
      else {
        return '#fff'
      }
    },
    getSelectedBorderColor(deal) {
      if (this.currentDeal && this.showDeal) {
        if (deal.id == this.currentDeal.id) {
          return '#808080'
        }
      }
    },
    setCurrentDeal(deal) {
      this.$store.dispatch('eggs/setCurrentDeal', deal)
      this.showDeal = true
    },
    async updateDeals() {
      this.showDeal = false
      await this.$store.dispatch('bid/getDeals')
    },
    status(deal) {
      switch (deal.status) {
        case 1:
          return 'Ожидает подтверждения фин. директора'
        case 2:
          return 'Ожидание загрузки документов, основание для платежа продавцу'
        case 3:
          return 'В процессе подтверждения на оплату продавцу'
        case 4:
          return 'В процессе оплаты и загрузки бухгалтером счета от продавца'
        case 5:
          return 'На контроле погрузки товара, ожидаем загрузку УПД'
        case 6:
          return 'Товар в пути, ожидаем запрос исходящей УПД'
        case 7:
          return 'Ожидание загрузки бухгалтером исходящей УПД'
        case 8:
          return 'На контроле разгрузки, в ожидании подписанной УПД'
        default:
          return 'Сделка закрыта'
      }
    }
  },
  computed: {
    deals() {
      return this.$store.state.bid.deals
    },
    currentDeal() {
      return this.$store.state.eggs.currentDeal
    }
  },
  created() {
    this.updateDeals()
  }
}
</script>
  
<style lang="scss" scoped>
ul {
  list-style-type: none;
  height: 81vh;
  overflow-y: scroll;
}

li {
  list-style-type: none;
  font-size: 12px;
}

.fade-enter-active {
  transition: all .4s ease;
}
.fade-leave-active {
  transition: all .4s ease;
}
.fade-enter, .fade-leave-to {
  transform: translateX(50px);
  opacity: 0;
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

  .seller {
    text-align: center;
    border: solid 2px #ebebeb;
    background-color: #099cf115;
    align-self: center;
    padding: 0 5px;
    border-radius: 5px;
  }

  .buyer {
    text-align: center;
    border: solid 2px #ebebeb;
    background-color: #4ce21115;
    align-self: center;
    padding: 0 5px;
    border-radius: 5px;
    margin-right: 0.15vw
  }

  .dates {
    border: solid 2px #ebebeb;
    align-self: center;
    border-radius: 5px;
  }

  .logic {
    text-align: center;
    border: solid 2px #4500a671;
    min-width: 30%;
    max-width: 40%;
    padding: 0 1vw;
    border-radius: 5px;
    margin-right: 0.15vw
  }

  .deals {
    width: 40vw;
    text-align: center;
    margin: 0.25vh 0.25vw;
    border: solid 1px #ff110069;
    border-radius: 5px;
    box-shadow: 10px 10px 5px #f5f5f5;
  }

  .component {
    margin: 0 0.25vw;

    &__buyer {
      margin-right: 0.9vw;
    }
  }

  .list-title {
    display: flex;
    position: relative;
    justify-content: center;
    align-items: center;
    font-size: 18px;
    width: 40vw;
    margin: 0.25vw;
    height: 32px;
    text-align: center;
    box-shadow: 3px 3px 5px #f5f5f5;
    background-color: #ff110015;
  }

  .list-item {
    border: solid 2px #f5f5f5;
    border-radius: 5px;
    margin-bottom: 0.25vh;
    padding: 0 0.5vw;
    box-shadow: 5px 5px 5px #f5f5f5;
    background-color: #fff;
    &:hover {
      cursor: pointer;
      border-color: #d5d5d5;
    }
  }

  .eggs-block {
    font-size: 10px;
    width: 16.5%;
    text-align: center;
    padding: 0 0.2vw;
    margin: 0 0.04vw;
    margin-bottom: 0.2vh;
    border: solid 1px;
    border-radius: 5px;
  }

  .refresh-button {
    position: absolute;
    right: 0;
    height: 100%;
    margin: 0;
    width: 120px;
    float: right;
    vertical-align: middle;
  }
</style>
  
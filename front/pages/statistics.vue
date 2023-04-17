<template>
  <div>
    <div class="flexbox__row">
      <div class="select-btn" @click="selectBuyers" v-bind:style="{ 'background-color': getBackgroundColor(showBuyers) }" v-bind:class="{ active: showBuyers }">Покупатели</div>
      <div class="select-btn" @click="selectSellers" v-bind:style="{ 'background-color': getBackgroundColor(showSellers) }" v-bind:class="{ active: showSellers }">Продавцы</div>
    </div>
    <div class="buyers" v-show="showBuyers">
      <ul class="buyers-list">
        <li v-for="buyer in buyers" @click="onBuyersClick(buyer)" :key="buyer.name" class="buyers-list__item flexbox flexbox__row flexbox__space-between">
          <div class="flexbox__row" style="display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
            <div style="padding-left: 10px;">{{ buyer.name }} / {{ buyer.inn }}</div>
          </div>
          <div class="flexbox__row">
            <b-icon icon="plus" v-if="buyer.balance >= 0"></b-icon>
            <b-icon icon="minus" v-else></b-icon>
            <div class="progress-bar" v-bind:style="{ 'justify-content': progressBarJustify(buyer.balance) }">
              <div class="progress-bar__text" v-if="buyer.balance >= 0">Баланс {{ buyer.balance }} ₽</div>
              <div class="progress-bar__text" v-else>Долг {{ Math.abs(buyer.balance) }} ₽</div>
              <div class="progress-bar__fill" v-bind:style="{ 'width': fillWidth(buyer.balance), 'background-color': fillBackgroundColor(buyer.balance) }"></div>
            </div>
          </div>
        </li>
      </ul>
      <transition name="fade">
        <Statistic v-if="this.$store.state.ca.traderData && showBuyer" :title="'Карточка покупателя'" @toggle-card="turnCardOff" style="float: right"/>
      </transition>
    </div>

    <div class="buyers" v-show="showSellers">
      <ul class="buyers-list">
        <li v-for="seller in sellers" @click="onSellersClick(seller)" :key="seller.name" class="buyers-list__item flexbox flexbox__row flexbox__space-between">
          <div class="flexbox__row" style="display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
            <div style="padding-left: 10px;">{{ seller.name }} / {{ seller.inn }}</div>
          </div>
          <div class="flexbox__row">
            <b-icon icon="plus" v-if="seller.balance >= 0"></b-icon>
            <b-icon icon="minus" v-else></b-icon>
            <div class="progress-bar" v-bind:style="{ 'justify-content': progressBarJustify(seller.balance) }">
              <div class="progress-bar__text" v-if="seller.balance >= 0">Баланс {{ seller.balance }} ₽</div>
              <div class="progress-bar__text" v-else>Долг {{ Math.abs(seller.balance) }} ₽</div>
              <div class="progress-bar__fill" v-bind:style="{ 'width': fillWidth(seller.balance), 'background-color': fillBackgroundColor(seller.balance) }"></div>
            </div>
          </div>
        </li>
      </ul>
      <transition name="fade">
        <Statistic v-if="this.$store.state.ca.traderData && showSeller" :title="'Карточка продавца'" @toggle-card="turnCardOff" style="float: right"/>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: "statistics",
  emits: ['toggle-card'],
  components: {
    Statistic: () => import("@/components/cards/Statistic")
  },
  data() {
    return {
      showBuyer: false,
      showSeller: false,
      showBuyers: true,
      showSellers: false,
      userRole: localStorage.getItem('userRole'),
    }
  },
  // middleware: 'auth',
  async created() {
    this.$store.dispatch('ca/getBuyersDebt')
    await this.$store.dispatch('ca/getSellersDebt')
  },
  methods: {
    turnCardOff() {
      this.showBuyer = false
      this.showSeller = false
    },
    async onBuyersClick(buyer) {
      if (this.showBuyer == false) {
        const tails = await this.$store.dispatch('ca/getTails', buyer.tails_id)
        const trader = buyer
        trader.tails = tails
        this.$store.dispatch('ca/setTraderData', trader)
        this.showBuyer = true
      }
      else {
        if (buyer.inn == this.$store.state.ca.traderData.inn) {
          this.showBuyer = false
          this.$store.dispatch('ca/setTraderData', null)
        }
        else {
          const tails = await this.$store.dispatch('ca/getTails', buyer.tails_id)
          const trader = buyer
          trader.tails = tails
          this.$store.dispatch('ca/setTraderData', trader)
        }
      }
    },
    async onSellersClick(seller) {
      if (this.showSeller == false) {
        const tails = await this.$store.dispatch('ca/getTails', seller.tails_id)
        const trader = seller
        trader.tails = tails
        this.$store.dispatch('ca/setTraderData', trader)
        this.showSeller = true
      }
      else {
        if (seller.inn == this.$store.state.ca.traderData.inn) {
          this.showSeller = false
          this.$store.dispatch('ca/setTraderData', null)
        }
        else {
          const tails = await this.$store.dispatch('ca/getTails', seller.tails_id)
          const trader = seller
          trader.tails = tails
          this.$store.dispatch('ca/setTraderData', trader)
        }
      }
    },
    progressBarJustify(balance) {
      const percent = balance / 30000000 * 100
      if (percent >= 0) {
        return 'end'
      }
      else {
        return 'start'
      }
    },
    fillWidth(balance) {
      const width = `${(Math.abs(balance) / 30000000) * 100}%`
      return width
    },
    fillBackgroundColor(balance) {
      const percent = (Math.abs(balance) / 30000000) * 100
      if (balance >= 0) {
        return '#73ff5780'
      }
      else {
        if (percent <= 100 && percent > 75 || percent > 100) {
            return '#eb1e1e80'
        }
        else if (percent <= 75 && percent > 50) {
            return '#f7ac2180'
        }
        else if (percent <= 50 && percent > 25) {
            return '#faf61583'
        }
        else if (percent >= 0 && percent <= 25) {
            return '#33d31380'
        }
      }
    },
    getPercent(limit, debt) {
      const percent = debt / limit * 100;
      return Math.round(percent)
    },
    getWidth(limit, debt) {
      const percent = debt / limit * 100;
      if (percent >= 100) return 100
      else return percent
    },
    getFillColor(percent){
      if (percent <= 100 && percent > 75 || percent > 100) {
        return '#eb1e1e80'
      }
      else if (percent <= 75 && percent > 50) {
        return '#f7ac2180'
      }
      else if (percent <= 50 && percent > 25) {
        return '#faf61583'
      }
      else if (percent >= 0 && percent <= 25) {
        return '#3af81480'
      }
    },
    getBackgroundColor(attr) {
      if (attr) return '#fff'
      else return '#e7e8ed'
    },
    selectBuyers() {
      this.showBuyer = false
      this.activeBuyer = {}
      this.showSellers = false
      this.showBuyers = true
    },
    selectSellers() {
      this.showBuyer = false
      this.activeBuyer = {}
      this.showBuyers = false
      this.showSellers = true
    }
  },
  computed: {
    buyers() {
      return this.$store.state.ca.buyersDebt
    },
    sellers() {
      return this.$store.state.ca.sellersDebt
    }
  }
}
</script>

<style lang="scss" scoped>
ul {
  list-style-type: none;
  height: 85vh;
  overflow-y: scroll;
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

.buyers {
  display: flex;
  justify-content: space-between;
  margin: 0;
  width: 81vw;
  gap: 2px;
  border: solid 2px #e7e8ed;
  border-radius: 0 5px 5px 5px;
}

.buyers-list {
  margin: 10px 5px;
  width: 80vw;
  font-size: 14px;

  &__item {
    width: 80vw;
    border-radius: 10px;
    margin: 0;

    cursor: pointer;
    background-color: #ffffff;
    border-bottom: 1px solid #f2f2f2;

    &:hover {
      background-color: #f2f2f2;
    }
  }
}

.progressBar {
  border: solid #e4e4e4 2px;
  text-align: center;
  border-radius: 20px;
  margin-left: 10px;
  width: 45vw;
  height: 28px;
}

.progress-bar {
  display: flex;
  border: solid 2px #e4e4e4;
  border-radius: 10px;
  height: 24px;
  width: 800px;
  position: relative;
  justify-content: end;

  &__text {
    position: absolute;
    text-align: center;
    margin: 0 auto;
    left: 50%;
    transform:translate(-50%, 0); 
  }
  &__fill {
    border-radius: 8px;
    width: 0;
  }
}

@media (min-width: 1200px) and (max-width: 1599px) {
  .progress-bar {
    width: 600px;
  }
}

.balance-bar {
  display: inline-flex;
  flex-direction: row;
  flex-flow: row;
  border: solid #e4e4e4 2px;
  text-align: center;
  border-radius: 20px;
  margin-left: 10px;
  width: 45vw;
  height: 12px;
}

.fill {
  height: 100%;
  width: 0;
  border-radius: 20px;
  
  &__left {
    border-radius: 20px 0 0 20px;
  }
  &__right {
    border-radius: 0 20px 20px 0;
  }
}

.fill-color {
  height: 100%;
  width: 100%;
  border-radius: 20px;
}

.select-btn {
  width: 180px;
  display: flex;
  justify-content: center;
  border: solid 2px #e7e8ed;
  border-bottom: 0;
  border-radius: 10px 10px 0 0;
  padding: 5px 15px;
  margin-right: 5px;
  cursor: pointer;
  position: relative;
}

.active {
  background-color: #fff;
}

.active:after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 5px;
  background-color: #fff;
}
</style>

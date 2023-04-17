<template>
  <div class="flexbox flexbox__row">
    <div class="flexbox__row">
      <div class="flexbox_column">
        <div class="list-title">
          Просчеты
          <b-button class="refresh-button" label="Обновить" type="is-warning" icon-left="refresh" @click="updateCalculates" />
        </div>
        <ul class="calcs">
          <li class="list-item flexbox flexbox__column" v-for="calc in calcs" :key="calc.id" @click="setCurrentCalc(calc)"
            v-bind:style="{'border-color': getSelectedBorderColor(calc)}">
            <div  class="flexbox__row flexbox__space-between" style="margin-right: 0.15vw">
              <div class="seller">{{ calc.seller_name }}</div>
              <div>{{ calc.title }} №{{ calc.id }}</div>
              <div class="buyer">{{ calc.buyer_name }}</div>
            </div>
            <div class="flexbox__row flexbox__space-between">
              <div style="margin-left: 1.5vw">{{ calc.delivery_date_from_seller }}</div>
              <div class="margin">{{ calc.margin }} ₽</div>
              <div style="margin-right: 1.5vw">{{ calc.delivery_date_to_buyer }}</div>
            </div>
            <div class="flexbox__row flexbox__space-between" style="width: 100%">
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(calc.cB), 'border-color': getBorderColor(calc.cB)}">
                <span v-show="calc.cB">CB: {{ calc.cB }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(calc.c0), 'border-color': getBorderColor(calc.c0)}">
                <span v-show="calc.c0">C0: {{ calc.c0 }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(calc.c1), 'border-color': getBorderColor(calc.c1)}">
                <span v-show="calc.c1">C1: {{ calc.c1 }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(calc.c2), 'border-color': getBorderColor(calc.c2)}">
                <span v-show="calc.c2">C2: {{ calc.c2 }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(calc.c3), 'border-color': getBorderColor(calc.c3)}">
                <span v-show="calc.c3">C3: {{ calc.c3 }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(calc.dirt), 'border-color': getBorderColor(calc.dirt)}">
                <span v-show="calc.dirt">Грязь: {{ calc.dirt }}</span>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div class="flexbox__row flexbox__space-between" style="width: 40vw">
      <transition name="fade">
        <div class="component" v-show="showCalc">
          <calculate v-if="currentCalc" />
        </div>
      </transition>
    </div>
  </div>
</template>
  
<script>
export default {
  name: "calculates",
  components: {
    calculate: () => import("@/components/tasks/calculate")
  },
  data() {
    return {
      showCalc: false,
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
    getSelectedBorderColor(calc) {
      if (this.currentCalc && this.showCalc) {
        if (calc.id == this.currentCalc.id) {
          return '#808080'
        }
      }
    },
    setCurrentCalc(calc) {
      this.$store.dispatch('eggs/setCurrentCalculate', calc)
      this.showCalc = true
    },
    async updateCalculates() {
      this.showCalc = false
      await this.$store.dispatch('bid/getCalculates')
    }
  },
  computed: {
    calcs() {
      return this.$store.state.bid.calculates
    },
    currentCalc() {
      return this.$store.state.eggs.currentCalculate
    }
  },
  created() {
    this.updateCalculates()
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

.seller {
  text-align: center;
  border: solid 2px #00a2ff5f;
  min-width: 30%;
  max-width: 40%;
  padding: 0 1vw;
  border-radius: 5px;
}

.buyer {
  text-align: center;
  border: solid 2px #48ff0054;
  min-width: 30%;
  max-width: 40%;
  padding: 0 1vw;
  border-radius: 5px;
  margin-right: 0.15vw
}

.calcs {
  width: 40vw;
  margin: 0.25vh 0.25vw;
  border: solid 1px #d7c90063;
  border-radius: 5px;
  box-shadow: 10px 10px 5px #f5f5f5;
}

.component {
  margin: 0 0.25vw;

  &__buyer {
    margin-right: 0.9vw;
  }
}

.margin {
  border-bottom: solid 2px #ff9d0093;
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
  background-color: #ffee0015;
  background-color: #d4c60015;
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
  vertical-align: center;
}
</style>
  
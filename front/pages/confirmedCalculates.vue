<template>
  <div class="flexbox flexbox__row">
    <div class="flexbox__row">
      <div class="flexbox_column">
        <div class="list-title">
          Подтвержденные просчеты
          <b-button class="refresh-button" label="Обновить" type="is-warning" icon-left="refresh" @click="updateConfCalculates" />
        </div>
        <ul class="conf-calcs">
          <li class="list-item flexbox flexbox__column" v-for="confCalculate in confCalcs" :key="confCalculate.id" @click="setCurrentConfCalc(confCalculate)"
            v-bind:style="{'border-color': getSelectedBorderColor(confCalculate)}">
            <div  class="flexbox__row flexbox__space-between" style="margin-right: 0.15vw">
              <div class="seller">{{ confCalculate.seller_name }}</div>
              <div>№{{ confCalculate.id }}</div>
              <div class="buyer">{{ confCalculate.buyer_name }}</div>
            </div>
            <div class="flexbox__row flexbox__space-between">
              <div style="margin-left: 3.7vw">{{ confCalculate.delivery_date_from_seller }}</div>
              <div class="logic" v-if=(confCalculate.current_logic)>{{ confCalculate.logic_name }}</div>
              <div style="margin-right: 4vw">{{ confCalculate.delivery_date_to_buyer }}</div>
            </div>
            <div class="flexbox__row flexbox__space-between" style="width: 100%">
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(confCalculate.cB), 'border-color': getBorderColor(confCalculate.cB)}">
                <span v-show="confCalculate.cB">CB: {{ confCalculate.cB }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(confCalculate.c0), 'border-color': getBorderColor(confCalculate.c0)}">
                <span v-show="confCalculate.c0">C0: {{ confCalculate.c0 }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(confCalculate.c1), 'border-color': getBorderColor(confCalculate.c1)}">
                <span v-show="confCalculate.c1">C1: {{ confCalculate.c1 }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(confCalculate.c2), 'border-color': getBorderColor(confCalculate.c2)}">
                <span v-show="confCalculate.c2">C2: {{ confCalculate.c2 }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(confCalculate.c3), 'border-color': getBorderColor(confCalculate.c3)}">
                <span v-show="confCalculate.c3">C3: {{ confCalculate.c3 }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(confCalculate.dirt), 'border-color': getBorderColor(confCalculate.dirt)}">
                <span v-show="confCalculate.dirt">Грязь: {{ confCalculate.dirt }}</span>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div class="flexbox__row flexbox__space-between" style="width: 40vw">
      <transition name="fade">
        <div class="component" v-if="showConfCalc">
          <confirmedCalculate @patch="confCalcPatched" />
        </div>
      </transition>
    </div>
  </div>
</template>
  
<script>
export default {
  name: "confirmedCalculates",
  components: {
    confirmedCalculate: () => import("@/components/tasks/confirmedCalculate")
  },
  data() {
    return {
      showConfCalc: false
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
    getSelectedBorderColor(confCalc) {
      if (this.currentConfCalc && this.showConfCalc) {
        if (confCalc.id == this.currentConfCalc.id) {
          return '#808080'
        }
      }
    },
    setCurrentConfCalc(confCalc) {
      this.$store.dispatch('eggs/setCurrentConfCalculate', confCalc)
      this.showConfCalc = true
    },
    async updateConfCalculates() {
      this.showConfCalc = false
      await this.$store.dispatch('bid/getConfCalculates')
    },
    async confCalcPatched() {
      await this.$store.dispatch('bid/getConfCalculates')
    }
  },
  computed: {
    confCalcs() {
      return this.$store.state.bid.confCalculates
    },
    currentConfCalc() {
      return this.$store.state.eggs.currentConfCalculate
    }
  },
  created() {
    this.updateConfCalculates()
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

.logic {
  text-align: center;
  border-bottom: solid 2px #4500a671;
  max-width: 40%;
  margin-right: 0.15vw
}

.conf-calcs {
  width: 40vw;
  text-align: center;
  margin: 0.25vh 0.25vw;
  border: solid 1px #ff7b0074;
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
  background-color: #ff7b0015;
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
  
<template>
  <div class="flexbox flexbox__column">
    <div class="flexbox__row">
      <div class="flexbox_column">
        <div class="list-title list-title__seller">
          Заявки от продавца
          <b-button class="refresh-button" label="Обновить" type="is-warning" icon-left="refresh" @click="updateAppsSeller" />
        </div>
        <ul class="sellers">
          <li class="list-item flexbox__column" v-for="app in appsFromSeller" :key="(app.title, app.id)" @click="setCurrentAppFromSeller(app)"
            v-bind:style="{'border-color': getSelectedBorderColor(app)}">
            <div class="flexbox__row flexbox__space-between" style="width: 100%" v-if="app.import_application">
              <div class="app-type app-type__import" v-show="app.import_application">Импорт</div>
            </div>
            <div style="margin-bottom: 0.1vh">
              <span style="width: 5vw">{{ app.seller_card_detail.name }}</span>
              <span class="region" v-show="app.region">{{ app.region }}</span>
              <div style="float: right">
                <span class="postponement" v-show="app.postponement_pay">{{ app.postponement_pay }}</span>
                <span style="float: right; margin-right: 0.15vw">{{ app.delivery_window_from }} --- {{ app.delivery_window_until }}</span>
              </div>
            </div>
            <div class="flexbox__row flexbox__space-between" style="width: 100%">
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(app.cB), 'border-color': getBorderColor(app.cB)}">
                <span v-show="app.cB">CB: {{ app.cB }} по {{ app.cB_cost }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(app.c0), 'border-color': getBorderColor(app.c0)}">
                <span v-show="app.c0">C0: {{ app.c0 }} по {{ app.c0_cost }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(app.c1), 'border-color': getBorderColor(app.c1)}">
                <span v-show="app.c1">C1: {{ app.c1 }} по {{ app.c1_cost }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(app.c2), 'border-color': getBorderColor(app.c2)}">
                <span v-show="app.c2">C2: {{ app.c2 }} по {{ app.c2_cost }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(app.c3), 'border-color': getBorderColor(app.c3)}">
                <span v-show="app.c3">C3: {{ app.c3 }} по {{ app.c3_cost }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(app.dirt), 'border-color': getBorderColor(app.dirt)}">
                <span v-show="app.dirt">Грязь: {{ app.dirt }} по {{ app.dirt_cost }}</span>
              </div>
            </div>
          </li>
        </ul>
      </div>
      <div class="flexbox__column">
        <div class="list-title list-title__buyer">
          Заявки от покупателя
          <b-button class="refresh-button" label="Обновить" type="is-warning" icon-left="refresh" @click="updateAppsBuyer" />
        </div>
        <ul class="buyers">
          <li class="list-item flexbox__column" v-for="app in appsFromBuyer" :key="(app.title, app.id)" @click="setCurrentAppFromBuyer(app)"
            v-bind:style="{'border-color': getSelectedBorderColor(app)}">
            <div style="margin-bottom: 0.1vh">
              <span style="width: 5vw">{{ app.buyer_card_detail.name }}</span>
              <span class="region" v-show="app.region">{{ app.region }}</span>
              <div style="float: right">
                <span class="postponement" v-show="app.postponement_pay">{{ app.postponement_pay }}</span>
                <span style="float: right; margin-right: 0.15vw">{{ app.delivery_window_from }} --- {{ app.delivery_window_until }}</span>
              </div>
            </div>
            <div class="flexbox__row flexbox__space-between" style="width: 100%">
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(app.cB), 'border-color': getBorderColor(app.cB)}">
                <span v-show="app.cB">CB: {{ app.cB }} по {{ app.cB_cost }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(app.c0), 'border-color': getBorderColor(app.c0)}">
                <span v-show="app.c0">C0: {{ app.c0 }} по {{ app.c0_cost }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(app.c1), 'border-color': getBorderColor(app.c1)}">
                <span v-show="app.c1">C1: {{ app.c1 }} по {{ app.c1_cost }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(app.c2), 'border-color': getBorderColor(app.c2)}">
                <span v-show="app.c2">C2: {{ app.c2 }} по {{ app.c2_cost }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(app.c3), 'border-color': getBorderColor(app.c3)}">
                <span v-show="app.c3">C3: {{ app.c3 }} по {{ app.c3_cost }}</span>
              </div>
              <div class="eggs-block" v-bind:style="{'background-color': getBackgroundColor(app.dirt), 'border-color': getBorderColor(app.dirt)}">
                <span v-show="app.dirt">Грязь: {{ app.dirt }} по {{ app.dirt_cost }}</span>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div class="flexbox__row flexbox__space-between" style="width: 81.75vw">
      <div class="component">
        <transition name="fade">
          <appSeller :appSeller="currentAppFromSeller" v-if="currentAppFromSeller" />
        </transition>
      </div>
      <div class="component component__buyer">
        <transition name="fade">
          <appBuyer :appBuyer="currentAppFromBuyer" v-if="currentAppFromBuyer" />
        </transition>
      </div>
    </div>
    <div class="calcButton" v-show="currentAppFromSeller && currentAppFromBuyer">
      <b-button type="is-success" @click="createCalc" :disabled="checkCategories()">Создать просчет</b-button>
    </div>
  </div>
</template>
  
<script>
import ModalCalcForm from '@/components/forms/ModalCalcForm'
export default {
  name: "apps",
  components: {
    appSeller: () => import("@/components/tasks/appSeller"),
    appBuyer: () => import("@/components/tasks/appBuyer")
  },
  data() {
    return {
      currentAppFromSeller: null,
      currentAppFromBuyer: null,
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
    getSelectedBorderColor(app) {
      if (app == this.currentAppFromBuyer || app == this.currentAppFromSeller) {
        return '#808080'
      }
    },
    setCurrentAppFromSeller(app) {
      if (this.currentAppFromSeller == app) {
        this.currentAppFromSeller = null
      }
      else {
        this.currentAppFromSeller = app
      }
    },
    setCurrentAppFromBuyer(app) {
      if (this.currentAppFromBuyer == app) {
        this.currentAppFromBuyer = null
      }
      else {
        this.currentAppFromBuyer = app
      }
    },
    async updateAppsSeller() {
      await this.$store.dispatch('bid/getAppsFromSeller')
      this.currentAppFromSeller = null
    },
    async updateAppsBuyer() {
      await this.$store.dispatch('bid/getAppsFromBuyer')
      this.currentAppFromBuyer = null
    },
    createCalc() {
      const apps = [this.currentAppFromSeller, this.currentAppFromBuyer]
      this.$buefy.modal.open({
        parent: this,
        component: ModalCalcForm,
        hasModalCard: true,
        trapFocus: true,
        props:{
          apps: apps
        }
      })
    },
    checkCategories() {
      if (this.currentAppFromSeller && this.currentAppFromBuyer) {
        if (this.currentAppFromSeller.cB && this.currentAppFromBuyer.cB) {
          return false
        }
        else if (this.currentAppFromSeller.c0 && this.currentAppFromBuyer.c0) {
          return false
        }
        else if (this.currentAppFromSeller.c1 && this.currentAppFromBuyer.c1) {
          return false
        }
        else if (this.currentAppFromSeller.c2 && this.currentAppFromBuyer.c2) {
          return false
        }
        else if (this.currentAppFromSeller.c3 && this.currentAppFromBuyer.c3) {
          return false
        }
        else if (this.currentAppFromSeller.dirt && this.currentAppFromBuyer.dirt) {
          return false
        }
        else {
          return true
        }
      }
    }
  },
  computed: {
    appsFromSeller() {
      return this.$store.state.bid.appsFromSeller
    },
    appsFromBuyer() {
      return this.$store.state.bid.appsFromBuyer
    }
  },
  async created() {
    this.updateAppsSeller()
    this.updateAppsBuyer()
  }
}
</script>
  
<style lang="scss" scoped>
ul {
  list-style-type: none;
  height: 48vh;
  overflow-y: scroll;
}

li {
  list-style-type: none;
  font-size: 12px;
}

.app-type {
  font-size: 10px;
  width: 100%;
  text-align: center;
  padding: 0;
  margin-bottom: 0.2vh;
  border: solid 1px #ebebeb;
  border-radius: 20px;

  &__import {
    background-color: #c411dc3f;
  }
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

.sellers {
  width: 40vw;
  margin: 0.25vh 0.25vw;
  border: solid 1px #00a2ff5f;
  border-radius: 5px;
  box-shadow: 10px 10px 5px #f5f5f5;
}

.buyers {
  width: 40vw;
  margin: 0.25vh 0.25vw;
  border: solid 1px #48ff0054;
  border-radius: 5px;
  box-shadow: 10px 10px 5px #f5f5f5;
}

.component {
  margin: 0 0.25vw;

  &__buyer {
    margin-right: 0.9vw;
  }
}

.fade-enter-active {
  transition: all .4s ease;
}
.fade-leave-active {
  transition: all .4s ease;
}
.fade-enter, .fade-leave-to {
  transform: translateY(50px);
  opacity: 0;
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
  box-shadow: 3px 3px 5px #f5f5f5;

  &__seller {
    background-color: #099cf115;
  }
  &__buyer {
    background-color: #4ce21115;
  }
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

.region {
  margin-left: 1vw;
  border: solid #c4c4c4 2px;
  border-radius: 5px;
  padding: 0 0.25vw;
}

.postponement {
  margin-right: 1vw;
  border: solid #ffa61fc0 2px;
  border-radius: 5px;
  padding: 0 0.25vw;
}

.eggs-block {
  font-size: 10px;
  width: 20%;
  text-align: center;
  padding: 0 0.2vw;
  margin: 0 0.04vw;
  margin-bottom: 0.2vh;
  border: solid 1px;
  border-radius: 5px;
}

.calcButton {
  text-align: center;
  margin: 2vh 2vw;
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
  
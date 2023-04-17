<template>
  <form action="" style="width: 1250px">
    <div class="modal-card" style="width: 1100px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Редактирование Подтвержденного просчета №{{confCalculate.id}}</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>

      <section class="modal-card-body is-fullwidth">
        <div class="flexbox flexbox__row flexbox__space-between" style="width: 100%">
          <div class="editButton" @click="editLogic = !editLogic" 
            v-bind:style="{'background-color': getBackground(editLogic)}"
            v-show="userRole != '4'">
            Логист
          </div>
          <div class="editButton" @click="editDates = !editDates" 
            v-bind:style="{'background-color': getBackground(editDates)}"
            v-show="userRole != '4'">
            Даты
          </div>
          <div class="editButton" @click="editEggs = !editEggs" 
            v-bind:style="{'background-color': getBackground(editEggs)}"
            v-show="userRole != '4'">
            Продукция
          </div>
          <div class="editButton" @click="editComment = !editComment" 
            v-bind:style="{'background-color': getBackground(editComment)}"
            v-show="userRole != '4'">
            Комментарий
          </div>
        </div>

        <div v-show="editLogic">
          <div class="flexbox flexbox__end" style="width: 100%">
            <div class="seller-delivery" @click="deliveryBySeller = !deliveryBySeller" v-bind:style="{'background-color': cashPayment(deliveryBySeller)}">Доставка от продавца</div>
          </div>
          <div v-show="!deliveryBySeller">
            <div class="card__row input-border" style="align-items: center; padding: 0 10px;">
              Логист: 
              <div v-if="logicName" class="card__info">
                {{ logicName }}
              </div>
              <div v-else-if="selectedLogic" class="card__info">
                {{ confCalculate.logic_name }}
              </div>
            </div>
            <b-dropdown :triggers="['hover']" aria-role="list" style="margin-bottom: 8px">
              <template #trigger>
                <b-button
                  v-model="currentLogic"  
                  label="Выберите логиста"
                  type="is-success is-light"
                  icon-right="menu-down"
                  rounded />
              </template>
    
            <b-dropdown-item aria-role="listitem" v-for="logic in logists" :key="logic.id" @click="selectLogist(logic)">
              <strong>{{ logic.name }}</strong></b-dropdown-item>
            </b-dropdown>
  
            <b-button type="is-success is-light" label="Создать логиста" rounded @click="createNewLogic"/>
    
            <div class="flexbox__row" style="width: 1060px">
              <div class="flexbox__row flexbox__space-between input-border">
                <div style="margin-left: 10px; margin-top: 8px;">Стоимость доставки ₽</div>
                <b-field style="width: 60%">
                  <b-input placeholder="Введите сумму" rounded v-model="deliveryCost"></b-input>
                </b-field>
              </div>
            </div>
  
            <div class="card__row input-border" style="align-items: center; padding-left: 10px;">Тип оплаты доставки: 
              <span class="card__info flexbox__row" style="width: 50%;">
                <div class="pay-type" @click="setDeliveryTypeOfPayment(20)" v-bind:style="{'background-color': getBackgroundColor(20)}">С НДС</div>
                <div class="pay-type" @click="setDeliveryTypeOfPayment(0)" v-bind:style="{'background-color': getBackgroundColor(0)}">Без НДС</div>
              </span>
            </div>
          </div>
        </div>
        <div v-show="editDates">
          <div class="card__row input-border" style="align-items: center; padding: 0 10px;">Дата погрузки: 
            <span class="card__info">
              {{ getStrDay(deliveryDateFromSeller) }}
            </span>
          </div>
          <div class="card__row input-border" style="align-items: center; padding: 0 10px;">Дата разгрузки: 
            <span class="card__info">
              {{ getStrDay(deliveryDateToBuyer) }}
            </span>
          </div>
          <b-button
            label="Изменить дату погрузки"
            type="is-success is-light"
            style="margin-bottom: 8px"
            @click="addLoadingDate = !addLoadingDate"
            rounded/>
          <b-button
            label="Изменить дату разгрузки"
            type="is-success is-light"
            style="margin-bottom: 8px"
            @click="addUnloadingDate = !addUnloadingDate"
            rounded/>

          <div class="flexbox flexbox__row input-border" style="justify-content: space-around; height: 450px; width: 100%;" v-show="addLoadingDate || addUnloadingDate">
            <div class="flexbox__column" style=" padding: 10px 20px;" v-show="addLoadingDate">
              <div class="changeDates">Новая дата погрузки</div>
              <div class="flexbox__row flexbox__space-between" style="margin-top: 15px">
                <b-datepicker
                  style="width: 360px;"
                  v-model="loadingDate"
                  inline>
                </b-datepicker>
              </div>
            </div>
            <div class="flexbox__column" style=" padding: 10px 20px;" v-show="addUnloadingDate">
              <div class="changeDates">Новая дата разгрузки</div>
              <div class="flexbox__row flexbox__space-between" style="margin-top: 15px">
                <b-datepicker
                  style="width: 360px;"
                  v-model="unloadingDate"
                  inline>
                </b-datepicker>
              </div>
            </div>
          </div>
        </div>
        <div v-show="editEggs" class="flexbox__column">
          <div class="flexbox__row" v-show="confCalculate.cB" style="width: 1060px">
            <div class="flexbox__row flexbox__space-between input-border">
              <div style="margin-left: 10px; margin-top: 8px; width: 45px">CB</div>
              <b-field class="my-b-input">
                <b-input placeholder="Количество (дес.)" rounded v-model="cB"></b-input>
              </b-field>

              <div style="margin-left: 10px; margin-top: 8px">Закупка ₽</div>
              <b-field class="my-b-input-cost">
                <b-input placeholder="Введите сумму" rounded type="text" v-model="sellerCBCost"></b-input>
              </b-field>

              <div style="margin-left: 10px; margin-top: 8px">Продажа ₽</div>
              <b-field class="my-b-input-cost">
                <b-input placeholder="Введите сумму" rounded v-model="buyerCBCost"></b-input>
              </b-field>
            </div>
          </div>

          <div class="flexbox__row" v-show="confCalculate.c0" style="width: 1060px">
            <div class="flexbox__row flexbox__space-between input-border">
              <div style="margin-left: 10px; margin-top: 8px; width: 45px">C0</div>
              <b-field class="my-b-input">
                <b-input placeholder="Количество (дес.)" rounded v-model="c0"></b-input>
              </b-field>

              <div style="margin-left: 10px; margin-top: 8px">Закупка ₽</div>
              <b-field class="my-b-input-cost">
                <b-input placeholder="Введите сумму" rounded v-model="sellerC0Cost"></b-input>
              </b-field>

              <div style="margin-left: 10px; margin-top: 8px">Продажа ₽</div>
              <b-field class="my-b-input-cost">
                <b-input placeholder="Введите сумму" rounded v-model="buyerC0Cost"></b-input>
              </b-field>
            </div>
          </div>

          <div class="flexbox__row" v-show="confCalculate.c1" style="width: 1060px">
            <div class="flexbox__row flexbox__space-between input-border">
              <div style="margin-left: 10px; margin-top: 8px; width: 45px">C1</div>
              <b-field class="my-b-input">
                <b-input placeholder="Количество (дес.)" rounded v-model="c1"></b-input>
              </b-field>

              <div style="margin-left: 10px; margin-top: 8px">Закупка ₽</div>
              <b-field class="my-b-input-cost">
                <b-input placeholder="Введите сумму" rounded v-model="sellerC1Cost"></b-input>
              </b-field>

              <div style="margin-left: 10px; margin-top: 8px">Продажа ₽</div>
              <b-field class="my-b-input-cost">
                <b-input placeholder="Введите сумму" rounded v-model="buyerC1Cost"></b-input>
              </b-field>
            </div>
          </div>

          <div class="flexbox__row" v-show="confCalculate.c2" style="width: 1060px">
            <div class="flexbox__row flexbox__space-between input-border">
              <div style="margin-left: 10px; margin-top: 8px; width: 45px">C2</div>
              <b-field class="my-b-input">
                <b-input placeholder="Количество (дес.)" rounded v-model="c2"></b-input>
              </b-field>

              <div style="margin-left: 10px; margin-top: 8px">Закупка ₽</div>
              <b-field class="my-b-input-cost">
                <b-input placeholder="Введите сумму" rounded v-model="sellerC2Cost"></b-input>
              </b-field>

              <div style="margin-left: 10px; margin-top: 8px">Продажа ₽</div>
              <b-field class="my-b-input-cost">
                <b-input placeholder="Введите сумму" rounded v-model="buyerC2Cost"></b-input>
              </b-field>
            </div>
          </div>

          <div class="flexbox__row" v-show="confCalculate.c3" style="width: 1060px">
            <div class="flexbox__row flexbox__space-between input-border">
              <div style="margin-left: 10px; margin-top: 8px; width: 45px">C3</div>
              <b-field class="my-b-input">
                <b-input placeholder="Количество (дес.)" rounded v-model="c3"></b-input>
              </b-field>

              <div style="margin-left: 10px; margin-top: 8px">Закупка ₽</div>
              <b-field class="my-b-input-cost">
                <b-input placeholder="Введите сумму" rounded v-model="sellerC3Cost"></b-input>
              </b-field>

              <div style="margin-left: 10px; margin-top: 8px">Продажа ₽</div>
              <b-field class="my-b-input-cost">
                <b-input placeholder="Введите сумму" rounded v-model="buyerC3Cost"></b-input>
              </b-field>
            </div>
          </div>

          <div class="flexbox__row" v-show="confCalculate.dirt" style="width: 1060px">
            <div class="flexbox__row flexbox__space-between input-border">
              <div style="margin-left: 10px; margin-top: 8px; width: 45px">Грязь</div>
              <b-field class="my-b-input">
                <b-input placeholder="Количество (дес.)" rounded v-model="dirt"></b-input>
              </b-field>

              <div style="margin-left: 10px; margin-top: 8px">Закупка ₽</div>
              <b-field class="my-b-input-cost">
                <b-input placeholder="Введите сумму" rounded v-model="sellerDirtCost"></b-input>
              </b-field>

              <div style="margin-left: 10px; margin-top: 8px">Продажа ₽</div>
              <b-field class="my-b-input-cost">
                <b-input placeholder="Введите сумму" rounded v-model="buyerDirtCost"></b-input>
              </b-field>
            </div>
          </div>

          <div style="width: 100%; height: 38px;">
            <div class="seller-delivery" @click="cash = !cash" v-bind:style="{'background-color': cashPayment(cash)}" style="float: right">
              Продажа за наличку
            </div>
          </div>

          <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; align-items: center;">
            <div style="margin-left: 10px">Отсрочка оплаты продавцу (дней):</div>
            <b-field class="my-b-input-cost" style="width: 50%;">
              <b-input placeholder="Введите кол-во дней" rounded v-model="postponementPayForUs"></b-input>
            </b-field>
          </div>

          <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; align-items: center;">
            <div style="margin-left: 10px">Отсрочка оплаты покупателю (дней):</div>
            <b-field class="my-b-input-cost" style="width: 50%;">
              <b-input placeholder="Введите кол-во дней" rounded v-model="postponementPayForBuyer"></b-input>
            </b-field>
          </div>
        </div>

        <div v-show="editComment">
          <div class="card__row">
            Комментарий подтвержденного просчета:
          </div>
          <b-field>
            <b-input v-model="comment" type="textarea" maxlength="255"></b-input>
          </b-field>
        </div>
      </section>

      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Подтвердить изменения"
          :loading="loading"
          type="is-success"
          @click="editConfCalc"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
import ModalCreateLogicForm from '@/components/forms/ModalCreateLogicForm'
export default {
  name: "ModalConfCalcEditForm",
  props: ['confCalculate'],
  data() {
    return {
      editLogic: false,
      editDates: false,
      editAdditionalExpense: false,
      editEggs: false,
      editComment: false,
      cB: this.confCalculate.cB,
      sellerCBCost: this.confCalculate.seller_cB_cost,
      buyerCBCost: this.confCalculate.buyer_cB_cost,
      c0: this.confCalculate.c0,
      sellerC0Cost: this.confCalculate.seller_c0_cost,
      buyerC0Cost: this.confCalculate.buyer_c0_cost,
      c1: this.confCalculate.c1,
      sellerC1Cost: this.confCalculate.seller_c1_cost,
      buyerC1Cost: this.confCalculate.buyer_c1_cost,
      c2: this.confCalculate.c2,
      sellerC2Cost: this.confCalculate.seller_c2_cost,
      buyerC2Cost: this.confCalculate.buyer_c2_cost,
      c3: this.confCalculate.c3,
      sellerC3Cost: this.confCalculate.seller_c3_cost,
      buyerC3Cost: this.confCalculate.buyer_c3_cost,
      dirt: this.confCalculate.dirt,
      sellerDirtCost: this.confCalculate.seller_dirt_cost,
      buyerDirtCost: this.confCalculate.buyer_dirt_cost,
      selectedLogic: this.confCalculate.current_logic,
      currentLogic: null,
      logicName: '',
      deliveryBySeller: this.confCalculate.delivery_by_seller,
      deliveryCost: this.confCalculate.delivery_cost,
      cash: this.confCalculate.cash,
      deliveryDateFromSeller: this.confCalculate.delivery_date_from_seller,
      deliveryDateToBuyer: this.confCalculate.delivery_date_to_buyer,
      deliveryTypeOfPayment: this.confCalculate.delivery_type_of_payment,
      comment: this.confCalculate.comment,
      postponementPayForUs: this.confCalculate.postponement_pay_for_us,
      postponementPayForBuyer: this.confCalculate.postponement_pay_for_buyer,
      addLoadingDate: false,
      addUnloadingDate: false,
      loadingDate: null,
      unloadingDate: null,
      loading: false,
      userRole: localStorage.getItem('userRole')
    }
  },
  methods: {
    selectLogist(logic) {
      this.logicName = logic.name
      this.currentLogic = logic
    },
    createNewLogic() {
      this.$buefy.modal.open({
        parent: this,
        component: ModalCreateLogicForm,
        hasModalCard: true,
        trapFocus: true
      })
    },
    getStrMonth(month) {
      switch (month) {
        case 0:
          return 'января'
        case 1:
          return 'февраля'
        case 2:
          return 'марта'
        case 3:
          return 'апреля'
        case 4:
          return 'мая'
        case 5:
          return 'июня'
        case 6:
          return 'июля'
        case 7:
          return 'августа'
        case 8:
          return 'сентября'
        case 9:
          return 'октября'
        case 10:
          return 'ноября'
        case 11:
          return 'декабря'
      }
    },
    getStrDay(dateStr) {
      const date = Date.parse(dateStr)
      const currentDate = new Date(date)
      return currentDate.getDate() + ' ' + this.getStrMonth(currentDate.getMonth()) + ' ' + currentDate.getFullYear()
    },
    checkForComma(eggsCost) {
      let eggCost = `${eggsCost}`
      if (eggCost.includes(',')) {
        eggCost = eggCost.replace(',', '.')
      }
      return parseFloat(eggCost)
    },
    async editConfCalc() {
      if (this.cB) {
        if (!this.sellerCBCost) {
          return alert('Вы не указали стоимость закупки категории СВ')
        }
        if (!this.buyerCBCost) {
          return alert('Вы не указали стоимость продажи категории СВ')
        }
      }
      if (this.c0) {
        if (!this.sellerC0Cost) {
          return alert('Вы не указали стоимость закупки категории С0')
        }
        if (!this.buyerC0Cost) {
          return alert('Вы не указали стоимость продажи категории С0')
        }
      }
      if (this.c1) {
        if (!this.sellerC1Cost) {
          return alert('Вы не указали стоимость закупки категории С1')
        }
        if (!this.buyerC1Cost) {
          return alert('Вы не указали стоимость продажи категории С1')
        }
      }
      if (this.c2) {
        if (!this.sellerC2Cost) {
          return alert('Вы не указали стоимость закупки категории С2')
        }
        if (!this.buyerC2Cost) {
          return alert('Вы не указали стоимость продажи категории С2')
        }
      }
      if (this.c3) {
        if (!this.sellerC3Cost) {
          return alert('Вы не указали стоимость закупки категории С3')
        }
        if (!this.buyerC3Cost) {
          return alert('Вы не указали стоимость продажи категории С3')
        }
      }
      if (this.dirt) {
        if (!this.sellerDirtCost) {
          return alert('Вы не указали стоимость закупки категории Грязь')
        }
        if (!this.buyerDirtCost) {
          return alert('Вы не указали стоимость продажи категории Грязь')
        }
      }
      this.loading = true
      const id = this.confCalculate.id
      const confCalc = {
        cB: this.cB,
        seller_cB_cost: this.sellerCBCost ? this.checkForComma(this.sellerCBCost) : 0,
        buyer_cB_cost: this.buyerCBCost ? this.checkForComma(this.buyerCBCost) : 0,
        c0: this.c0,
        seller_c0_cost: this.sellerC0Cost ? this.checkForComma(this.sellerC0Cost) : 0,
        buyer_c0_cost: this.buyerC0Cost ? this.checkForComma(this.buyerC0Cost) : 0,
        c1: this.c1,
        seller_c1_cost: this.sellerC1Cost ? this.checkForComma(this.sellerC1Cost) : 0,
        buyer_c1_cost: this.buyerC1Cost ? this.checkForComma(this.buyerC1Cost) : 0,
        c2: this.c2,
        seller_c2_cost: this.sellerC2Cost ? this.checkForComma(this.sellerC2Cost) : 0,
        buyer_c2_cost: this.buyerC2Cost ? this.checkForComma(this.buyerC2Cost) : 0,
        c3: this.c3,
        seller_c3_cost: this.sellerC3Cost ? this.checkForComma(this.sellerC3Cost) : 0,
        buyer_c3_cost: this.buyerC3Cost ? this.checkForComma(this.buyerC3Cost) : 0,
        dirt: this.dirt,
        seller_dirt_cost: this.sellerDirtCost ? this.checkForComma(this.sellerDirtCost) : 0,
        buyer_dirt_cost: this.buyerDirtCost ? this.checkForComma(this.buyerDirtCost) : 0,
        delivery_type_of_payment: this.deliveryTypeOfPayment,
        postponement_pay_for_us: this.postponementPayForUs,
        postponement_pay_for_buyer: this.postponementPayForBuyer,
        cash: this.cash,
        delivery_cost: this.deliveryCost,
        comment: this.comment
      }
      if (this.addLoadingDate) {
        calcEdit.delivery_date_from_seller = this.loadingDate.getDate() + '.' + (this.loadingDate.getMonth() + 1) + '.' + this.loadingDate.getFullYear()
      }
      if (this.addUnloadingDate) {
        calcEdit.delivery_date_to_buyer = this.unloadingDate.getDate() + '.' + (this.unloadingDate.getMonth() + 1) + '.' + this.unloadingDate.getFullYear()
      }
      if (this.currentLogic) {
        confCalc.current_logic = this.currentLogic.id
      }
      const updatedConfCalc = await this.$store.dispatch('eggs/patchConfCalc', [confCalc, id])
        .finally(() => this.loading = false, setTimeout(this.update, 1000))
      if (!updatedConfCalc) return
      await this.$store.dispatch('eggs/setCurrentConfCalculate', updatedConfCalc)
      this.$emit('close')
    },
    async update() {
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
    },
    getBorderColor(attr) {
      if (attr) {
        return '#41e33882'
      }
    },
    getBackground(attr) {
      if (attr) {
        return '#41e3382a'
      }
    },
    setDeliveryTypeOfPayment(type) {
      this.deliveryTypeOfPayment = type
    },
    getBackgroundColor(payType) {
      if (payType == this.deliveryTypeOfPayment) {
        return '#48c78e'
      }
      else {
        return '#fff'
      }
    },
    cashPayment(cash) {
      if (cash) {
        return 'hsl(151, 63%, 54%)'
      }
      else {
        return '#fff'
      }
    },
  },
  mounted() {
    this.$store.dispatch('ca/getLogists')
  },
  computed: {
    logists() {
      return this.$store.state.ca.logists
    }
  },
  created() {
    if (this.userRole == '4') {
      this.editLogic = true
      this.editDates = true
    }
  }
}
</script>

<style lang="scss" scoped>
form {
  font-family: 'Montserrat';
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

.card {
  width: 100%;
  
  &__row {
    display: flex;
    justify-content: space-between;
    margin-bottom: .5rem;
    border-bottom: solid #f5f5f5 2px;
  }
  &__info {
    overflow-wrap: break-word;
    max-width: 500px;
    font-weight: 500;
    margin-left: 1rem;
  }
}

.editButton {
  width: 24%;
  padding: 1vh 1vw;
  text-align: center;
  border: 3px solid #ebebeb;
  margin-bottom: 2vh;
  background-color: #f5f5f5;
  border-radius: 20px;
  cursor: pointer;
  &:hover {
    border-color: hsl(151, 63%, 54%);
    background-color: #41e33817;
  }
}

.pay-type {
  height: 40px;
  display: flex;
  border: solid 2px #ebebeb;
  width: 50%;
  font-weight: 400;
  border-radius: 20px;
  cursor: pointer;
  justify-content: center;
  align-items: center;
}

.input-border {
  border: solid 2px #ebebeb;
  border-radius: 20px;
  width: 1060px;
  height: 44px;
  margin-bottom: 5px;
}

.my-b-input {
  width: 20%;
}

.my-b-input-cost {
  width: 20%;
}

.payType {
  display: inline-flex;
  border: solid 2px #ebebeb;
  font-weight: 400;
  text-align: center;
  border-radius: 20px;
  padding: 5px;
  cursor: pointer;
}

.categories__calendar {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
  margin-bottom: 5px;
}

.seller-delivery {
  display: flex;
  cursor: pointer;
  width: 50%;
  height: 40px;
  border: solid 2px #ebebeb;
  border-radius: 20px;
  text-align: center;
  margin-bottom: 5px;
  align-items: center;
  justify-content: center;
}

.changeDates {
  display: flex;
  color: white;
  justify-content: center;
  font-size: 18px;
  border-radius: 15px;
  background-color: #823bf570;
}
</style>

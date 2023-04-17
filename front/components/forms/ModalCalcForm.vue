<template>
  <form action="" style="width: 1250px">
    <div class="modal-card" style="width: 1100px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Создание просчета</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>
      <section class="modal-card-body is-fullwidth flexbox">
        <div class="flexbox__column">
          <div class="flexbox__row" style="margin-bottom: 15px">
            <appSeller :appSeller="apps[0]" style="width:530px"/>
            <appBuyer :appBuyer="apps[1]" style="width:530px"/>
          </div>
          
          <div class="flexbox__column">
            <div class="flexbox__row" v-show="(apps[0].cB && apps[1].cB)" style="width: 1060px">
              <div class="flexbox__row flexbox__space-between input-border">
                <div style="margin-left: 10px; margin-top: 8px; width: 45px">CB</div>
                <b-field class="my-b-input">
                  <b-input placeholder="Количество (дес.)" rounded v-model="cB"></b-input>
                </b-field>

                <div style="margin-left: 10px; margin-top: 8px">Закупка ₽</div>
                <b-field class="my-b-input-cost">
                  <b-input placeholder="Введите сумму" rounded v-model="sellerCBCost"></b-input>
                </b-field>

                <div style="margin-left: 10px; margin-top: 8px">Продажа ₽</div>
                <b-field class="my-b-input-cost">
                  <b-input placeholder="Введите сумму" rounded v-model="buyerCBCost"></b-input>
                </b-field>
              </div>
            </div>

            <div class="flexbox__row" v-show="(apps[0].c0 && apps[1].c0)" style="width: 1060px">
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

            <div class="flexbox__row" v-show="(apps[0].c1 && apps[1].c1)" style="width: 1060px">
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

            <div class="flexbox__row" v-show="(apps[0].c2 && apps[1].c2)" style="width: 1060px">
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

            <div class="flexbox__row" v-show="(apps[0].c3 && apps[1].c3)" style="width: 1060px">
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

            <div class="flexbox__row" v-show="(apps[0].dirt && apps[1].dirt)" style="width: 1060px">
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

            <div class="flexbox flexbox__row flexbox__space-between input-border" style="height: 450px; width: 100%;">
              <div class="flexbox__column" style=" padding: 10px 20px;">
                <div class="changeDates">Изменение даты погрузки и разгрузки</div>
                <div class="flexbox__row flexbox__space-between" style="margin-top: 15px">
                  <b-datepicker
                    style="width: 360px;"
                    v-model="dates"
                    inline
                    range>
                  </b-datepicker>
                </div>
              </div>
              <div class="flexbox__column" style="width: 656px; padding: 10px 20px;">
                <div class="flexbox flexbox__end" style="width: 100%">
                  <div class="seller-delivery" @click="deliveryBySeller = !deliveryBySeller" v-bind:style="{'background-color': cashPayment(deliveryBySeller)}">Доставка от продавца</div>
                </div>

                <div v-show="!deliveryBySeller" style="width: 100%">
                  <div class="flexbox__row" style="width: 100%">
                    <div class="flexbox__row flexbox__space-between input-border">
                      <div style="margin-left: 10px; margin-top: 8px;">Приблизительная стоимость доставки ₽</div>
                      <b-field style="width: 40%">
                        <b-input placeholder="Введите сумму" rounded v-model="averageDeliveryCost"></b-input>
                      </b-field>
                    </div>
                  </div>
      
                  <div class="flexbox__row" style="width: 100%">
                    <div class="flexbox__row flexbox__space-between input-border">
                      <div style="margin-left: 10px; margin-top: 8px;">Тип оплаты доставки</div>
                      <div style="width: 50%" class="flexbox__row">
                        <div class="payType" @click="deliveryTypeOfPayment = 20" v-bind:style="{'background-color': getBackgroundColor(20)}">С НДС</div>
                        <div class="payType" @click="deliveryTypeOfPayment = 0" v-bind:style="{'background-color': getBackgroundColor(0)}">Без НДС</div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="flexbox flexbox__end" style="width: 100%;">
                  <div class="payType" @click="cash = !cash" v-bind:style="{'background-color': cashPayment(cash)}">Оплата наличкой</div>
                </div>
              </div>
            </div>
            
            Комментарий
            <b-field>
              <b-input v-model="comment" type="textarea" maxlength="255"></b-input>
            </b-field>
          </div>
        </div>
      </section>
      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Создать просчет"
          :loading="loading"
          type="is-success"
          @click="sendCalcOrder"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
export default {
  name: "ModalCalcForm",
  props: ['apps'],
  components: {
    appSeller: () => import("@/components/tasks/appSeller"),
    appBuyer: () => import("@/components/tasks/appBuyer")
  },
  data() {
    return {
        loading: false,
        comment: '',
        deliveryBySeller: false,
        averageDeliveryCost: null,
        deliveryTypeOfPayment: 20,
        cB: null,
        sellerCBCost: null,
        buyerCBCost: null,
        c0: null,
        sellerC0Cost: null,
        buyerC0Cost: null,
        c1: null,
        sellerC1Cost: null,
        buyerC1Cost: null,
        c2: null,
        sellerC2Cost: null,
        buyerC2Cost: null,
        c3: null,
        sellerC3Cost: null,
        buyerC3Cost: null,
        dirt: null,
        sellerDirtCost: null,
        buyerDirtCost: null,
        dates: null,
        cash: false
    }
  },
  methods: {
    checkForComma(eggsCost) {
      let eggCost = `${eggsCost}`
      if (eggCost.includes(',')) {
        eggCost = eggCost.replace(',', '.')
      }
      return parseFloat(eggCost)
    },
    async sendCalcOrder() {
      if (!this.cB && !this.c0 && !this.c1 && !this.c2 && !this.c3 && !this.dirt) {
        return alert('Вы пытаетесь создать пустой просчет')
      }
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
      if (!this.dates) {
        return alert('Вы не указали дату погрузки и разгрузки')
      }
      if (!this.deliveryBySeller && !this.averageDeliveryCost) {
        return alert('Вы не указали приблизительную стоимость доставки')
      }

      const calc = {
        application_from_seller: this.apps[0].id,
        seller: this.apps[0].seller_card_detail.inn,
        loading_address: this.apps[0].loading_address,
        postponement_pay_for_us: this.apps[0].postponement_pay,
        application_from_buyer: this.apps[1].id,
        buyer: this.apps[1].buyer_card_detail.inn,
        unloading_address: this.apps[1].unloading_address,
        postponement_pay_for_buyer: this.apps[1].postponement_pay,
        delivery_by_seller: this.deliveryBySeller,
        delivery_cost: Number(this.averageDeliveryCost),
        delivery_type_of_payment: this.deliveryTypeOfPayment,
        cB: this.cB ? this.cB : 0,
        seller_cB_cost: this.sellerCBCost ? this.checkForComma(this.sellerCBCost) : 0,
        buyer_cB_cost: this.buyerCBCost ? this.checkForComma(this.buyerCBCost) : 0,
        c0: this.c0 ? this.c0 : 0,
        seller_c0_cost: this.sellerC0Cost ? this.checkForComma(this.sellerC0Cost) : 0,
        buyer_c0_cost: this.buyerC0Cost ? this.checkForComma(this.buyerC0Cost) : 0,
        c1: this.c1 ? this.c1 : 0,
        seller_c1_cost: this.sellerC1Cost ? this.checkForComma(this.sellerC1Cost) : 0,
        buyer_c1_cost: this.buyerC1Cost ? this.checkForComma(this.buyerC1Cost) : 0,
        c2: this.c2 ? this.c2 : 0,
        seller_c2_cost: this.sellerC2Cost ? this.checkForComma(this.sellerC2Cost) : 0,
        buyer_c2_cost: this.buyerC2Cost ? this.checkForComma(this.buyerC2Cost) : 0,
        c3: this.c3 ? this.c3 : 0,
        seller_c3_cost: this.sellerC3Cost ? this.checkForComma(this.sellerC3Cost) : 0,
        buyer_c3_cost: this.buyerC3Cost ? this.checkForComma(this.buyerC3Cost) : 0,
        dirt: this.dirt ? this.dirt : 0,
        seller_dirt_cost: this.sellerDirtCost ? this.checkForComma(this.sellerDirtCost) : 0,
        buyer_dirt_cost: this.buyerDirtCost ? this.checkForComma(this.buyerDirtCost) : 0,
        comment: this.comment ? this.comment : '',
        cash: this.cash
      }
      if (this.dates) {
        calc.delivery_date_from_seller = this.dates[0].getDate() + '.' + (this.dates[0].getMonth() + 1) + '.' + this.dates[0].getFullYear()
        calc.delivery_date_to_buyer = this.dates[1].getDate() + '.' + (this.dates[1].getMonth() + 1) + '.' + this.dates[1].getFullYear()
      }
      this.loading = true
      const success = await this.$store.dispatch('eggs/postCalc', calc)
        .finally(() => this.loading = false, setTimeout(this.update, 1000))
      if (!success) return
      this.$emit('close')
      await this.$router.push('/')
    },
    update() {
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
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
        return '#48c78e'
      }
      else {
        return '#fff'
      }
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
  &__row {
    display: flex;
    justify-content: space-between;
    align-items: center;
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

.categories__calendar {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
  margin-top: 20px;
  padding-bottom: 20px;
}

.payType {
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
  width: 100%;
  height: 44px;
  margin-bottom: 5px;
}

.my-b-input {
  width: 20%;
}

.my-b-input-cost {
  width: 20%;
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
  font-size: 17px;
  border-radius: 15px;
  background-color: #823bf570;
}
</style>

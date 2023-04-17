<template>
  <form action="" style="width: 1250px">
    <div class="modal-card" style="width: 1100px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Редактирование Просчета №{{calculate.id}}</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>

      <section class="modal-card-body is-fullwidth flexbox">
        <div class="flexbox__column">
          <div class="flexbox__row" v-show="calculate.cB" style="width: 1060px">
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

          <div class="flexbox__row" v-show="calculate.c0" style="width: 1060px">
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

          <div class="flexbox__row" v-show="calculate.c1" style="width: 1060px">
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

          <div class="flexbox__row" v-show="calculate.c2" style="width: 1060px">
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

          <div class="flexbox__row" v-show="calculate.c3" style="width: 1060px">
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

          <div class="flexbox__row" v-show="calculate.dirt" style="width: 1060px">
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

          <div class="flexbox flexbox__end" style="width: 100%">
            <div class="seller-delivery" @click="deliveryBySeller = !deliveryBySeller" v-bind:style="{'background-color': cashPayment(deliveryBySeller)}">Доставка от продавца</div>
          </div>

          <div v-show="!deliveryBySeller">
            <div class="flexbox__row" style="width: 1060px">
              <div class="flexbox__row flexbox__space-between input-border">
                <div style="margin-left: 10px; margin-top: 8px;">Приблизительная стоимость доставки ₽</div>
                <b-field style="width: 60%">
                  <b-input placeholder="Введите сумму" rounded v-model="averageDeliveryCost"></b-input>
                </b-field>
              </div>
            </div>

            <div class="flexbox__row" style="width: 1060px">
              <div class="flexbox__row flexbox__space-between input-border">
                <div style="margin-left: 10px; margin-top: 8px;">Тип оплаты доставки</div>
                <div style="width: 50%" class="flexbox__row">
                  <div class="payType" @click="deliveryTypeOfPayment = 20" v-bind:style="{'background-color': getBackgroundColor(20)}">С НДС</div>
                  <div class="payType" @click="deliveryTypeOfPayment = 0" v-bind:style="{'background-color': getBackgroundColor(0)}">Без НДС</div>
                </div>
              </div>
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
            <div class="flexbox__column" style="border-left: solid 2px #ebebeb;  padding: 10px 20px;">
              <div class="flexbox__column" style="gap: 10px">
                <div class="card__row input-border" style="align-items: center; padding: 0 10px; width: 100%; margin-bottom: 10px;" v-if="dates">Новая дата погрузки
                  <span class="card__info">
                    {{ getStrDay(dates[0]) }}
                  </span>
                </div>
                <div class="card__row input-border" style="align-items: center; padding: 0 10px; width: 100%; margin-bottom: 10px;" v-else>Дата погрузки
                  <span class="card__info">
                    {{ getStrDay(calculate.delivery_date_from_seller) }}
                  </span>
                </div>
                
                <div class="card__row input-border" style="align-items: center; padding: 0 10px; width: 100%; margin-bottom: 10px;" v-if="dates">Новая дата разгрузки
                  <span class="card__info">
                    {{ getStrDay(dates[1]) }}
                  </span>
                </div>
                <div class="card__row input-border" style="align-items: center; padding: 0 10px; width: 100%; margin-bottom: 10px;" v-else>Дата разгрузки
                  <span class="card__info">
                    {{ getStrDay(calculate.delivery_date_to_buyer) }}
                  </span>
                </div>
  
                <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; align-items: center; margin-bottom: 10px;">
                  <div style="margin-left: 10px">Отсрочка оплаты продавцу (дней):</div>
                  <b-field class="my-b-input-cost" style="width: 40%;">
                    <b-input placeholder="Введите кол-во дней" rounded v-model="postponementPayForUs"></b-input>
                  </b-field>
                </div>
  
                <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; align-items: center; margin-bottom: 10px;">
                  <div style="margin-left: 10px">Отсрочка оплаты покупателю (дней):</div>
                  <b-field class="my-b-input-cost" style="width: 40%;">
                    <b-input placeholder="Введите кол-во дней" rounded v-model="postponementPayForBuyer"></b-input>
                  </b-field>
                </div>
              
                <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; align-items: center; margin-bottom: 10px;">
                  <div style="margin-left: 10px">Продажа за наличку</div>
                  <b-checkbox :value="true"
                    type="is-success"
                    size="is-medium"
                    v-model="cash">
                  </b-checkbox>
                </div>
              </div>
            </div>
          </div>
        
          Комментарий:
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
          @click="editCalc"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
export default {
  name: "ModalCalcEditForm",
  props: ['calculate'],
  data() {
    return {
      cB: this.calculate.cB,
      sellerCBCost: this.calculate.seller_cB_cost,
      buyerCBCost: this.calculate.buyer_cB_cost,
      c0: this.calculate.c0,
      sellerC0Cost: this.calculate.seller_c0_cost,
      buyerC0Cost: this.calculate.buyer_c0_cost,
      c1: this.calculate.c1,
      sellerC1Cost: this.calculate.seller_c1_cost,
      buyerC1Cost: this.calculate.buyer_c1_cost,
      c2: this.calculate.c2,
      sellerC2Cost: this.calculate.seller_c2_cost,
      buyerC2Cost: this.calculate.buyer_c2_cost,
      c3: this.calculate.c3,
      sellerC3Cost: this.calculate.seller_c3_cost,
      buyerC3Cost: this.calculate.buyer_c3_cost,
      dirt: this.calculate.dirt,
      sellerDirtCost: this.calculate.seller_dirt_cost,
      buyerDirtCost: this.calculate.buyer_dirt_cost,
      averageDeliveryCost: this.calculate.delivery_cost,
      deliveryTypeOfPayment: this.calculate.delivery_type_of_payment,
      comment: this.calculate.comment,
      dates: null,
      loading: false,
      cash: this.calculate.cash,
      deliveryBySeller: this.calculate.delivery_by_seller,
      postponementPayForUs: this.calculate.postponement_pay_for_us,
      postponementPayForBuyer: this.calculate.postponement_pay_for_buyer
    }
  },
  methods: {
    cashPayment(cash) {
      if (cash) {
        return 'hsl(151, 63%, 54%)'
      }
      else {
        return '#fff'
      }
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
    async editCalc() {
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
      const data = {
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
        delivery_cost: this.deliveryBySeller ? 0 : this.averageDeliveryCost,
        delivery_type_of_payment: this.deliveryBySeller ? 0 : this.deliveryTypeOfPayment,
        postponement_pay_for_us: this.postponementPayForUs,
        postponement_pay_for_buyer: this.postponementPayForBuyer,
        comment: this.comment,
        cash: this.cash,
        delivery_by_seller: this.deliveryBySeller
      }
      if (this.dates) {
        data.delivery_date_from_seller = this.dates[0].getDate() + '.' + (this.dates[0].getMonth() + 1) + '.' + this.dates[0].getFullYear()
        data.delivery_date_to_buyer = this.dates[1].getDate() + '.' + (this.dates[1].getMonth() + 1) + '.' + this.dates[1].getFullYear()
      }
      this.loading = true
      const id = this.calculate.id
      const updatedCalc =  await this.$store.dispatch('eggs/patchCalc', [data, id])
        .finally(() => this.loading = false, setTimeout(this.update, 1000))
      if (!updatedCalc) return
      await this.$store.dispatch('eggs/setCurrentCalculate', updatedCalc)
      this.$emit('close')
    },
    update() {
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
    },
    getBackgroundColor(payType) {
      if (payType == this.deliveryTypeOfPayment) {
        return 'hsl(151, 63%, 54%)'
      }
      else {
        return '#fff'
      }
    },
    setDeliveryTypeOfPayment(type) {
      this.deliveryTypeOfPayment = type
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

.categories__calendar {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
  margin-bottom: 5px;
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

.changeDates {
  display: flex;
  color: white;
  justify-content: center;
  font-size: 17px;
  border-radius: 15px;
  background-color: #823bf570;
}
</style>

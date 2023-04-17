<template>
  <div class="card box" v-if="traderData">
    <div style="display: flex; flex-direction: row; justify-content: center;">
      <div class="debt-button debt-button__form1" v-bind:class="{ 'active-btn': getBoolForBtn(form) }" @click="btnClick(true)">Форма 1</div>
      <div class="debt-button debt-button__form2" v-bind:class="{ 'active-btn': getBoolForBtn(!form) }" @click="btnClick(false)">Форма 2</div>
    </div>

    <div v-if="title == 'Карточка покупателя'">
      <div class="progressBar" style="margin: 0 auto; margin-bottom: 5px;" v-show="form" v-if="traderData.balance_form_one < 0">
      <div class="fill" v-bind:style="{ width: getPercent(traderData.pay_limit, Math.abs(traderData.balance_form_one)) + '%', 
          backgroundColor: getFillColor(getPercent(traderData.pay_limit, Math.abs(traderData.balance_form_one)))}">
          <div style="font-size: 14px; width: 45vw; z-index: 100; vertical-align: center;">
            Долг: {{ Math.abs(traderData.balance_form_one) }} ₽ из {{ traderData.pay_limit }} ₽ {{ getPercentText(traderData.pay_limit, Math.abs(traderData.balance_form_one)) }}%
          </div>
        </div>
      </div>
      <div class="progressBar" style="margin: 0 auto; margin-bottom: 5px;" v-show="form" v-else>
        <div class="fill" v-bind:style="{ width: '100%', backgroundColor: '#73ff5780' }">
          <div style="font-size: 14px; width: 45vw; z-index: 100; vertical-align: center;">
            Баланс: {{ Math.abs(traderData.balance_form_one) }} ₽
          </div>
        </div>
      </div>
  
      <div class="progressBar" v-show="!form" v-if="traderData.balance_form_two < 0" style="margin: 0 auto">
        <div class="fill" v-bind:style="{ width: getPercent(traderData.pay_limit_cash, Math.abs(traderData.balance_form_two)) + '%', 
          backgroundColor: getFillColor(getPercent(traderData.pay_limit_cash, Math.abs(traderData.balance_form_two)))}">
          <div style="font-size: 14px; width: 45vw; z-index: 100; vertical-align: center;">
            Долг: {{ Math.abs(traderData.balance_form_two) }} ₽ из {{ traderData.pay_limit_cash }} ₽ {{ getPercentText(traderData.pay_limit_cash, Math.abs(traderData.balance_form_two)) }}%
          </div>
        </div>
      </div>
      <div class="progressBar" style="margin: 0 auto; margin-bottom: 5px;" v-show="!form" v-else>
        <div class="fill" v-bind:style="{ width: '100%', backgroundColor: '#73ff5780' }">
          <div style="font-size: 14px; width: 45vw; z-index: 100; vertical-align: center;">
            Баланс: {{ Math.abs(traderData.balance_form_two) }} ₽
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="title == 'Карточка продавца'">
      <div class="progressBar" style="margin: 0 auto; margin-bottom: 5px;" v-show="form" v-if="traderData.balance_form_one < 0">
      <div class="fill" v-bind:style="{ width: getPercent(30000000, Math.abs(traderData.balance_form_one)) + '%', 
          backgroundColor: getFillColor(getPercent(30000000, Math.abs(traderData.balance_form_one)))}">
          <div style="font-size: 14px; width: 45vw; z-index: 100; vertical-align: center;">
            Долг: {{ Math.abs(traderData.balance_form_one) }} ₽
          </div>
        </div>
      </div>
      <div class="progressBar" style="margin: 0 auto; margin-bottom: 5px;" v-show="form" v-else>
        <div class="fill" v-bind:style="{ width: '100%', backgroundColor: '#73ff5780' }">
          <div style="font-size: 14px; width: 45vw; z-index: 100; vertical-align: center;">
            Баланс: {{ Math.abs(traderData.balance_form_one) }} ₽
          </div>
        </div>
      </div>
      <div class="progressBar" v-show="!form" v-if="traderData.balance_form_two < 0" style="margin: 0 auto">
        <div class="fill" v-bind:style="{ width: getPercent(30000000, Math.abs(traderData.balance_form_two)) + '%', 
          backgroundColor: getFillColor(getPercent(30000000, Math.abs(traderData.balance_form_two)))}">
          <div style="font-size: 14px; width: 45vw; z-index: 100; vertical-align: center;">
            Долг: {{ Math.abs(traderData.balance_form_two) }} ₽
          </div>
        </div>
      </div>
      <div class="progressBar" style="margin: 0 auto; margin-bottom: 5px;" v-show="!form" v-else>
        <div class="fill" v-bind:style="{ width: '100%', backgroundColor: '#73ff5780' }">
          <div style="font-size: 14px; width: 45vw; z-index: 100; vertical-align: center;">
            Баланс: {{ Math.abs(traderData.balance_form_two) }} ₽
          </div>
        </div>
      </div>
    </div>
    
    <div v-show="debtDeals.length > 0">
      <div class="debt">Задолженности по сделкам</div>
      <ul class="dealDebt" style="margin: 0" v-show="debtDeals.length > 0">
        <li v-for="deal in debtDeals" class="dealDebtItem" :key="deal.id" @click="goToDeal(deal.id)">
          <div class="flexbox flexbox__row flexbox__space-between" style="width: 100%;">
            <div>Сделка №{{ deal.id }}</div>
            <div class="progressDealDebt" v-bind:style="{ 'border-color': deal.marker }">
              <div class="fill" style="background-color: #e1e1e1; align-items: center; color: hsl(0deg, 0%, 29%)" v-bind:style="{ width: getPercent(deal.deal_buyer_debt_UPD, (deal.deal_buyer_debt_UPD - deal.current_deal_buyer_debt)) + '%'}">
                <div class="text-in-fill" style="font-size: 14px; height: 24px; padding: auto 0;">Оплачено: {{ deal.deal_buyer_debt_UPD - deal.current_deal_buyer_debt }} ₽ из {{ deal.deal_buyer_debt_UPD }} ₽</div>
              </div>
            </div>
          </div>
        </li>
      </ul> 
    </div>

    <div v-show="Object.keys(dealPayments).length > 0">
      <div class="payments" style="height: 40px; background-color: #f5f5f5;">Платежи</div>
      <div class="payments" style="padding: 0 20px; margin: 0">
        <div style="width: 37%;">Номер</div>
        <div style="width: 25%; text-align: center;">Дата</div>
        <div style="width: 38%; text-align: end;">Сумма</div>
      </div>
      <ul class="payments-list">
        <li v-for="payment in dealPayments" :key="payment.document_number" class="flexbox flexbox__column payment-on-deal">
          <div class="flexbox__row flexbox__space-between" style="width: 100%; padding: 0 10px">
            <div style="width: 37%;">№{{ payment.number }}</div>
            <div style="width: 25%; text-align: center;">от {{ payment.date }}</div>
            <div style="width: 38%; text-align: end;">{{ payment.total_amount || payment.pay_quantity }} ₽</div>
          </div>
        </li>
      </ul>
    </div>

    <div v-show="Object.keys(traderData.tails.tail_dict_json).length > 0 || Object.keys(traderData.tails.tail_dict_json_cash).length.length > 0">
      <div class="payments" style="height: 40px; background-color: #f5f5f5;">Депозит</div>
      <div class="payments" style="padding: 0 20px; margin: 0; justify-content: space-between;">
        <div style="width: 37%;">Номер</div>
        <div style="width: 25%; text-align: center;">Дата</div>
        <div style="width: 38%; text-align: end;">Сумма</div>
      </div>
      <ul class="payments-list" v-if="form">
        <li v-for="tail in traderData.tails.tail_dict_json" :key="tail.number" class="flexbox flexbox__column payment-on-deal">
          <div class="flexbox__row flexbox__space-between" style="width: 100%; padding: 0 10px">
            <div style="width: 30%;">№{{ tail.number }}</div>
            <div style="width: 18%; text-align: center;">от {{ tail.date }}</div>
            <div class="pay-btn" @click="useTails(traderData.tails.tail_dict_json, tail)" v-bind:style="{ 'background-color': checkDebtDeals() }">Использовать</div>
            <div  style="width: 10%; text-align: end;">{{ tail.total_amount }} ₽</div>
          </div>
        </li>
      </ul>
      <ul class="payments-list" v-else>
        <li v-for="tail in traderData.tails.tail_dict_json_cash" :key="tail.number" class="flexbox flexbox__column payment-on-deal">
          <div class="flexbox__row flexbox__space-between" style="width: 100%; padding: 0 10px">
            <div style="width: 30%;">№{{ tail.number }}</div>
            <div style="width: 20%; text-align: center;">от {{ tail.date }}</div>
            <div  style="width: 25%; text-align: end;">{{ tail.total_amount }} ₽</div>
            <div class="pay-btn" @click="useTails(traderData.tails.tail_dict_json_cash, tail)" v-bind:style="{ 'background-color': checkDebtDeals() }">Использовать</div>
          </div>
        </li>
      </ul>
    </div>

    <div class="border" style="margin-top: 10px; cursor: pointer; font-weight: 100;" @click="showCard = !showCard">{{ title }}</div>
    <div class="card__container" v-show="showCard">
      <div class="card__info">
        <div class="card__info-name">Название</div>
        <div>{{ traderData.name || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Инн</div>
        <div>{{ traderData.inn || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Контактное лицо</div>
        <div>{{ traderData.contact_person || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Телефон</div>
        <div>{{ traderData.phone || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Email</div>
        <div>{{ traderData.email || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Способ Оплаты</div>
        <div>{{ traderData.paymentType || 'Не указан' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Комментарий</div>
        <div>{{ traderData.comment || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Менеджер</div>
        <div>{{ traderData.manager_details || '-' }}</div>
      </div>
    </div>

    <div class="border" style="cursor: pointer; font-weight: 100;" @click="showRequisites = !showRequisites">Реквизиты компании</div>
    <div class="card__container" v-show="showRequisites" v-if="traderData.current_requisites">
      <div class="card__info">
        <div class="card__info-name">Ген Директор</div>
        <div>{{ traderData.current_requisites.general_manager || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Название Банка</div>
        <div>{{ traderData.current_requisites.bank_name || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Бик Банка</div>
        <div>{{ traderData.current_requisites.bic_bank || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Кор. счет</div>
        <div>{{ traderData.current_requisites.cor_account || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Расчетный счет</div>
        <div>{{ traderData.current_requisites.customers_pay_account || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Юр. адрес</div>
        <div>{{ traderData.current_requisites.legal_address || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Факт. адрес</div>
        <div>{{ traderData.current_requisites.physical_address || '-' }}</div>
      </div>
    </div>
    <div class="card__container" v-show="showRequisites" v-else>
      <div class="card__info">
        <div class="card__info-name">Ген Директор</div>
        <div>{{ traderData.general_manager || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Название Банка</div>
        <div>{{ traderData.bank_name || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Бик Банка</div>
        <div>{{ traderData.bic_bank || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Кор. счет</div>
        <div>{{ traderData.cor_account || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Расчетный счет</div>
        <div>{{ traderData.customers_pay_account || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Юр. адрес</div>
        <div>{{ traderData.legal_address || '-' }}</div>
      </div>
      <div class="card__info">
        <div class="card__info-name">Факт. адрес</div>
        <div>{{ traderData.physical_address || '-' }}</div>
      </div>
    </div>
    <div class="card__button-wrapper" style="margin: 0 auto; margin-top: 20px; min-width: 200px">
      <b-button type="is-success" @click="entryPayment">Платеж по Форме 1</b-button>
      <b-button type="is-success" @click="entryPaymentCash">Платеж по Форме 2</b-button>
    </div>
  </div>
</template>
  
<script>
import ModalPaymentForm from "@/components/forms/ModalPaymentForm"
import ModalPaymentCashForm from "@/components/forms/ModalPaymentCashForm"
import ModalDepositPay from "@/components/forms/ModalDepositPay"
export default {
  name: "Statistic",
  props: ['title'],
  data() {
    return {
      showCard: false,
      showRequisites: false,
      form: true,
    }
  },
  computed: {
    traderData() {
      return this.$store.state.ca.traderData
    },
    debtDeals() {
      if (this.traderData.debt_deals) {
        if (this.form) {
          const deals = this.traderData.debt_deals.filter(el => el.cash == false)
          if (deals.length > 0) {
            return deals
          }
          else {
            return []
          }
        }
        else {
          const deals = this.traderData.debt_deals.filter(el => el.cash == true)
          if (deals.length > 0) {
            return deals
          }
          else {
            return []
          }
        }
      }
      else {
        return []
      }
    },
    dealPayments() {
      let dealPayments
      if (this.traderData.current_contract) {
        dealPayments = this.traderData.current_contract.data_number_json
      }
      else {
        dealPayments = this.traderData.data_number_json
      }
      for (let key in dealPayments) {
        dealPayments[key].payment_time = key
      }
      return dealPayments
    },

  },
  methods: {
    useTails(object, tail) {
      if (this.debtDeals.length <= 0) return
      const uuid = Object.keys(object).find(key => object[key] === tail)
      const trader = this.traderData
      this.$buefy.modal.open({
        parent: this,
        component: ModalDepositPay,
        hasModalCard: true,
        trapFocus: true,
        props:{
          tail: tail,
          form: this.form,
          uuid: uuid,
          trader: trader,
          buyer: this.title == 'Карточка покупателя' ? true : false
        }
      })
      this.$emit('toggle-card')
    },
    checkDebtDeals() {
      if (this.debtDeals.length > 0) {
        return 'hsl(151, 63%, 54%)'
      }
      else {
        return '#dedede'
      }
    },
    btnClick(bool) {
      this.form = bool
      if (bool) {
        this.debtDeals = this.debtDealsForm1
      }
      else {
        this.debtDeals = this.debtDealsForm2
      }
    },
    getBoolForBtn(bool) {
      if (bool) {
        return true
      }
      else {
        return false
      }
    },
    async goToDeal(id) {
      const deal = await this.$store.dispatch('eggs/getModel', id)
      await this.$store.dispatch('eggs/setCurrentDeal', deal)
      this.$router.push('/Deal')
    },
    async entryPayment() {
      const acceptedRoles = ['6', '7', '8']
      const userRole = localStorage.getItem('userRole')
      if (!acceptedRoles.includes(userRole)) {
        return alert('Доступ запрещен')
      }
      const password = prompt('Введите пароль')
      if (password == '') {
        return alert('Доступ запрещен')
      }
      const checkPassword = await this.$store.dispatch('user/masterPassword', password)
      if (!checkPassword) {
        return alert('Доступ запрещен')
      }
      const buyer = this.traderData
      this.$buefy.modal.open({
        parent: this,
        component: ModalPaymentForm,
        hasModalCard: true,
        trapFocus: true,
        props:{
          trader: buyer,
          buyer: this.title == 'Карточка покупателя' ? true : false
        }
      })
      this.$emit('toggle-card')
    },
    async entryPaymentCash() {
      const acceptedRoles = ['6', '7', '8']
      const userRole = localStorage.getItem('userRole')
      if (!acceptedRoles.includes(userRole)) {
        return alert('Доступ запрещен')
      }
      const password = prompt('Введите пароль')
      if (password == '') {
        return alert('Доступ запрещен')
      }
      const checkPassword = await this.$store.dispatch('user/masterPassword', password)
      if (!checkPassword) {
        return alert('Доступ запрещен')
      }
      const buyer = this.traderData
      this.$buefy.modal.open({
        parent: this,
        component: ModalPaymentCashForm,
        hasModalCard: true,
        trapFocus: true,
        props:{
          trader: buyer,
          buyer: this.title == 'Карточка покупателя' ? true : false
        }
      })
      this.$emit('toggle-card')
    },
    getPercent(limit, debt) {
      const percent = debt / limit * 100;
      if (percent > 100) {
        return 100
      }
      return Math.round(percent)
    },
    getPercentText(limit, debt) {
      const percent = debt / limit * 100;
      return Math.round(percent)
    },
    getFillColor(percent) {
      if (percent > 75) {
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
  }
}
</script>
  
<style lang="scss" scoped>
ul {
  list-style-type: none;
  max-height: 250px;
  overflow-y: scroll;
}

.card {
  width: 100%;
  background-color: #f9f9f9;

  &__row {
    display: flex;
    justify-content: space-between;
    margin-bottom: .5rem;
    border-bottom: solid #f5f5f5 2px;
  }
  // &__info {
  //   overflow-wrap: break-word;
  //   max-width: 500px;
  //   font-weight: 1000;
  //   margin-left: 1rem;
  // }
  &__button-wrapper{
    display: flex;
    justify-content: center;
    border-radius: 10px;
    padding: 7px 5px;
    gap: 5px;
    background-color: #fff;
    border: solid 2px #f3f3f3;
  }
  &__container {
    flex-direction: column;
    flex-flow: column;
    justify-content: center;
    align-items: center;
    background-color: #fff;
    border: solid 2px #f3f3f3;
    border-top: 0;
    border-radius: 10px;
    padding: 7px 5px;
    margin-bottom: 10px;
  }
  &__info {
    display: inline-flex;
    flex-flow: row;
    justify-content: space-between;
    height: 28px;
    width: 100%;
    border-bottom: solid 1.5px #f3f3f3;
    border-radius: 5px;
    padding: 0 10px;
    margin-bottom: 5px;
  }
  &__info-name {
    color: #c4c4c4;
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

.border {
  display: flex;
  height: 30px;
  color: #7b7b7b;
  font-weight: 500;
  justify-content: center;
  align-content: center;
  border: solid #f5f5f5 2px;
  border-radius: 10px;
  background-color: #fff;
  margin-top: 10px;

  &:hover {
    cursor: pointer;
    color: #1e6ac8e8;
  }
}

.debt {
  display: flex;
  height: 28px;
  justify-content: center;
  align-items: center;
  color: #7b7b7b;
  background-color: #ff11000e;
  background-color: #fff;
  border: solid #ebebeb 2px;
  border-radius: 10px;
  margin-top: 5px;
  gap: 5px;
}

.pay-btn {
  color: #fff;
  // background-color: hsl(151, 63%, 54%);
  border-radius: 15px;
  padding: 0 10px;
  cursor: pointer;
}

.debt-button {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fff;
  border: solid 2px #ebebeb;
  // outline: solid 15px red;
  
  height: 35px;
  width: 250px;
  padding: 0 5px;
  margin-bottom: 10px;

  &__form1 {
    border-radius: 20px 0 0 20px;
  }

  &__form2 {
    border-radius: 0 20px 20px 0;
  }

  &:hover {
    cursor: pointer;
    border-color: #c1c1c1;
  }
}

.active-btn {
  color: #fff;
  background-color: hsl(153deg, 53%, 53%);
}

.dealDebt {
  padding-top: 5px;
  background-color: #fff;
  border: solid 2px #ebebeb;
  border-top: 0;
  border-radius: 10px;
}

.dealDebtItem {
  border-bottom: solid 1px #cfcfcf;
  border-radius: 5px;
  padding: 0 10px; 
  margin-bottom: 3px;

  &:hover {
    cursor: pointer;
    background-color: #f5f5f5;
    // color: #1e6ac8e8;
  }
}

.progressBar {
  border: solid #e4e4e4;
  background-color: #fff;
  text-align: center;
  border-radius: 20px;
  width: 45vw;
  height: 28px;
}

.progressDealDebt {
  border: solid 1px #e4e4e4;
  background-color: #fff;
  text-align: center;
  border-radius: 20px;
  height: 24px;
}

@media (min-width: 1600px) {
  .progressDealDebt {
    width: 650px;
  }
  .text-in-fill {
    width: 650px;
  }
}

@media (min-width: 1200px) and (max-width: 1599px) {
  .progressDealDebt {
    width: 450px;
  }
  .text-in-fill {
    width: 450px;
  }
}

.fill {
  height: 100%;
  width: 0;
  border-radius: 20px;
}

.fill-color {
  height: 100%;
  width: 100%;
  border-radius: 20px;
}

.payments {
  display: flex;
  height: 28px;
  margin-top: 5px;
  justify-content: center;
  align-items: center;
  color: #7b7b7b;
  background-color: #fff;
  border: solid #ebebeb 2px;
  border-radius: 10px;
}

.payments-list {
  margin: 0;
  width: 100%;
  background-color: #fff;
  border: solid 2px #ebebeb;
  border-top: 0;
  border-radius: 10px;
}

.payment-on-deal {
  padding: 0 10px;
  border-bottom: solid 1px #ebebeb;
  font-size: 14px;
  border-top: 0;
  border-radius: 5px;
}
</style>
  
<template>
  <div>
    <div class="card box" style="width: 40vw" v-if="confCalc">
      <div style="background-color: #fff; border-radius: 10px;">
        <h4 class="title has-text-centered border-title" @click="showConfCalc = !showConfCalc">{{ `Подтвержденный просчет №${confCalc.id}` || '' }}</h4>
      </div>

      <div class="conf-calculate conf-calculate__title">Продукция</div>
      <CalcTable :calc="confCalc" />

      <div class="conf-calculate__container">
        <div class="conf-calculate__info ca" v-show="currentUserRole != 4" @click="showExpenseInfo()">
          <div class="conf-calculate__info-name">Доп. расход</div>
          <div>{{ confCalc.expense_total || 0 }} ₽</div>
        </div>
        <div class="conf-calculate__info" v-if="confCalc.delivery_by_seller">
          <div class="conf-calculate__info-name">Доставка</div>
          <div>От продавца</div>
        </div>
        <div v-else>
          <div class="conf-calculate__info">
            <div class="conf-calculate__info-name">Стоимость доставки</div>
            <div>{{ confCalc.delivery_cost || 0 }} ₽</div>
          </div>
        </div>
        <div class="conf-calculate__info" v-show="currentUserRole != 4">
          <div class="conf-calculate__info-name">Маржа</div>
          <div>{{ confCalc.margin || 0 }} ₽</div>
        </div>
        <div class="conf-calculate__info" v-show="currentUserRole != 4 && confCalc.cash">
          <div class="conf-calculate__info-name">Продажа</div>
          <div>За наличные</div>
        </div>
      </div>

      <div class="conf-calculate conf-calculate__title" v-show="!confCalc.delivery_by_seller">Логист</div>
      <div class="conf-calculate__container" v-show="!confCalc.delivery_by_seller">
        <div class="conf-calculate__info ca" @click="showLogicInfo(confCalc.current_logic)">
          <div class="conf-calculate__info-name">Название</div>
          <div class="conf-calculate__scroll">{{ confCalc.logic_name }}</div>
        </div>
        <div class="conf-calculate__info">
          <div class="conf-calculate__info-name">ИНН</div>
          <div>{{ confCalc.logic_inn }}</div>
        </div>
        <div class="conf-calculate__info">
          <div class="conf-calculate__info-name">Тип оплаты доставки</div>
          <div>{{ paymentType() }}</div>
        </div>
      </div>

      <div class="conf-calculate conf-calculate__title">Контрагенты</div>
      <div class="conf-calculate conf-calculate__container">
        <div class="conf-calculate__attr" style="display: inline-flex; justify-content: space-between; width: 100%; padding: 0 10px;">
          <div class="ca-name">Продавец</div>
          <div>Название</div>
          <div class="ca-name" style="text-align: end;">Покупатель</div>
        </div>
        <div class="conf-calculate__row">
          <div class="conf-calculate__item conf-calculate__seller ca scroll" @click="showSellerInfo(confCalc.seller)">{{ confCalc.seller_name }}</div>
          <div class="conf-calculate__item conf-calculate__buyer ca scroll" style="text-align: end;" @click="showBuyerInfo(confCalc.buyer)">{{ confCalc.buyer_name }}</div>
        </div>
        <div class="conf-calculate__attr">ИНН</div>
        <div class="conf-calculate__row">
          <div class="conf-calculate__item conf-calculate__seller">{{ confCalc.seller }}</div>
          <div class="conf-calculate__item conf-calculate__buyer" style="text-align: end;">{{ confCalc.buyer }}</div>
        </div>
        <div class="conf-calculate__attr">Адрес погрузки/разгрузки</div>
        <div class="conf-calculate__row">
          <div class="conf-calculate__item conf-calculate__seller scroll">{{ confCalc.loading_address }}</div>
          <div class="conf-calculate__item conf-calculate__buyer scroll" style="text-align: end;">{{ confCalc.unloading_address }}</div>
        </div>
        <div class="conf-calculate__attr">Дата погрузки/разгрузки</div>
        <div class="conf-calculate__row">
          <div class="conf-calculate__item conf-calculate__seller">{{ getStrDay(confCalc.delivery_date_from_seller) }}</div>
          <div class="conf-calculate__item conf-calculate__buyer" style="text-align: end;">{{ getStrDay(confCalc.delivery_date_to_buyer) }}</div>
        </div>
        <div class="conf-calculate__attr">Отсрочка оплаты</div>
        <div class="conf-calculate__row">
          <div class="conf-calculate__item conf-calculate__seller">{{ postponementPayForUs }}</div>
          <div class="conf-calculate__item conf-calculate__buyer" style="text-align: end;">{{ postponementPayForBuyer }}</div>
        </div>
      </div>

      <div class="conf-calculate__container">
        <div class="conf-calculate__info">
          <div class="conf-calculate__info-name">Автор</div>
          <div>{{ confCalc.owner_name }}</div>
        </div>
        <div class="conf-calculate__info" v-show="confCalc.comment">
          <div class="conf-calculate__info-name">Комментарий</div>
          <div class="conf-calculate__info-scroll scroll" style="text-align: end;">{{ confCalc.comment }}</div>
        </div>
      </div>

      <div class="card__button-wrapper">
        <b-button type="is-success" @click="confirm" style="margin-right: 5px" v-if="confCalc.calc_ready && currentUserRole != '4'">Создать Сделку</b-button>
        <b-button type="is-success" @click="setReadyStatus" style="margin-right: 5px" v-else-if="!confCalc.calc_ready && currentUserRole != '4' && confCalc.logic_confirmed">Отпр. на подтверждение</b-button>
        <b-button type="is-success" @click="addLogic" style="margin-right: 5px" v-if="!confCalc.current_logic && (currentUserRole == '4' || currentUserRole == '6' || currentUserRole == '8')">Добавить логиста</b-button>
        <b-button type="is-success" @click="confirmLogic" style="margin-right: 5px" v-if="!confCalc.logic_confirmed && (currentUserRole == '4' || currentUserRole == '6' || currentUserRole == '8')" :disabled="!confCalc.current_logic">Подтвердить</b-button>
        <b-dropdown position="is-top-right">
          <template #trigger>
            <b-button label="Действия" type="is-info is-light" icon-right="menu-up" />
          </template>
          <b-dropdown-item style="padding: 0; margin-bottom: 3px;">
              <b-button type="is-warning" @click="makeNote" label="Замечание" style="width: 100%;" />
            </b-dropdown-item>
          <b-dropdown-item style="padding: 0; margin-bottom: 3px;">
            <b-button type="is-warning" @click="addExpense" label="Доп. расход" style="width: 100%;" />
          </b-dropdown-item>
          <b-dropdown-item style="padding: 0; margin-bottom: 3px;">
            <b-button type="is-success is-light" @click="editConfCalc" label="Редактировать" style="width: 100%;" />
          </b-dropdown-item>
          <b-dropdown-item style="padding: 0; margin-bottom: 3px;" v-show="canDelete()">
            <b-button type="is-danger is-light" @click="toggleIsActive" label="Удалить" style="width: 100%;" />
          </b-dropdown-item>
        </b-dropdown>
      </div>
    </div>
    
    <div v-show="showSellerCard" style="float: right">
      <SellerInfo :trader-data="currentSeller"/>
    </div>

    <div v-show="showBuyerCard" style="float: right">
      <BuyerInfo :trader-data="currentBuyer"/>
    </div>

    <div v-show="showLogicCard" style="float: right">
      <LogicInfo :trader-data="currentLogic"/>
    </div>

    <div v-show="showExpense" v-if="confCalc.expense_detail_json" style="float: right">
      <expense :expenseList="confCalc.expense_detail_json"/>
    </div>
  </div>
</template>

<script>
import ModalLogicForm from "@/components/forms/ModalLogic"
import ModalDatesForm from "@/components/forms/ModalDates"
import ModalConfCalcEditForm from "@/components/editForms/ModalConfCalcEditForm"
import addExpense from "@/components/addExpense"
import note from '@/components/note'
export default {
  name: 'ConfirmedCalculate',
  components: {
    SellerInfo: () => import("@/components/cards/SellerInfo"),
    BuyerInfo: () => import("@/components/cards/BuyerInfo"),
    LogicInfo: () => import("@/components/cards/LogicInfo"),
    expense: () => import("@/components/expense")
  },
  data() {
    return {
      result: false,
      showConfCalc: true,
      showSeller: true,
      showBuyer: true,
      showLogist: true,
      currentSeller: null,
      currentBuyer: null,
      currentLogic: null,
      currentExpense: null,
      showBuyerCard: false,
      showSellerCard: false,
      showLogicCard: false,
      showExpense: false,
      currentUserRole: localStorage.getItem('userRole'),
    }
  },
  methods: {
    makeNote() {
      if (this.currentUserRole == '4') {
        return alert('Доступ запрещен')
      }
      this.$buefy.modal.open({
        parent: this,
        component: note,
        hasModalCard: true,
        trapFocus: true,
        props:{
          task: this.confCalc,
          title: 'Подтвержденному просчету'
        }
      })
    },
    canDelete() {
      const acceptedRoles = ['6', '8']
      if (acceptedRoles.includes(this.currentUserRole)) {
        return true
      }
      else {
        return false
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
    confirm() {
      this.result = confirm('Создать сделку?')
      this.postDeal()
    },
    editConfCalc() {
      if (this.currentUserRole == '4' && this.confCalc.delivery_by_seller) {
        return alert('Доставка осуществляется продавцом')
      }
      this.$buefy.modal.open({
        parent: this,
        component: ModalConfCalcEditForm,
        hasModalCard: true,
        trapFocus: true,
        props:{
          confCalculate: this.confCalc
        }
      })
    },
    addExpense() {
      if (this.currentUserRole == '4') {
        return alert('Доступ запрещен')
      }
      this.$buefy.modal.open({
        parent: this,
        component: addExpense,
        hasModalCard: true,
        trapFocus: true,
        props:{
          task: this.confCalc,
          title: `Подтвержденного просчета №${this.confCalc.id}`
        }
      })
    },
    addLogic() {
      const confCalculate = this.confCalc
      this.$buefy.modal.open({
        parent: this,
        component: ModalLogicForm,
        hasModalCard: true,
        trapFocus: true,
        props:{
          confCalculate: confCalculate
        }
      })
    },
    addDates() {
      const confCalculate = this.confCalc
      this.$buefy.modal.open({
        parent: this,
        component: ModalDatesForm,
        hasModalCard: true,
        trapFocus: true,
        props:{
          confCalculate: confCalculate
        }
      })
    },
    async showSellerInfo(seller_inn) {
      const token = localStorage.getItem('access_token')
      const seller = await this.$axios.get(`eggs/seller_card/${seller_inn}/`, {headers: {Authorization: `Bearer ${token}`}})
      this.currentSeller = seller.data
      this.showExpense = false
      this.showBuyerCard = false
      this.showLogicCard = false
      if (this.currentSeller.inn == seller.data.inn) {
        this.showSellerCard = !this.showSellerCard
      }
      else {
        this.currentSeller = seller.data, this.showSellerCard = true
      }
    },
    async showBuyerInfo(buyer_inn) {
      const token = localStorage.getItem('access_token')
      const buyer = await this.$axios.get(`eggs/buyer_card/${buyer_inn}/`, {headers: {Authorization: `Bearer ${token}`}})
      this.currentBuyer = buyer.data
      this.showExpense = false
      this.showSellerCard = false
      this.showLogicCard = false
      if (this.currentBuyer.inn == buyer.data.inn) {
        this.showBuyerCard = !this.showBuyerCard
      }
      else {
        this.currentBuyer = buyer.data, this.showBuyerCard = true
      }
    },
    async showLogicInfo(logic) {
      if (!logic) return
      this.showExpense = false
      this.showBuyerCard = false
      this.showSellerCard = false
      if (this.currentLogic) {
        this.showLogicCard = !this.showLogicCard
      }
      else {
        this.currentLogic = await this.$store.dispatch('ca/getCurrentLogic', logic)
        this.showLogicCard = true
      }
    },
    showExpenseInfo() {
      if (this.confCalc.expense_total == 0) return
      this.showBuyerCard = false
      this.showSellerCard = false
      this.showLogicCard = false
      this.showExpense = !this.showExpense
    },
    async setReadyStatus() {
      if (!this.confCalc.current_logic) {
        return alert('Вы не указали логиста')
      }
      await this.$store.dispatch('eggs/patchConfCalcReadyStatus', this.confCalc.id)
      .then(async () => setTimeout(this.update, 1000))
      this.$router.push('/')
    },
    async confirmLogic() {
      const id = this.confCalc.id
      const confCalc = {
        logic_confirmed: true
      }
      const updatedConfCalc = await this.$store.dispatch('eggs/patchConfCalc', [confCalc, id, false])
      // const updatedConfCalc = await this.$store.dispatch('eggs/getModel', id)
      await this.$store.dispatch('eggs/setCurrentConfCalculate', updatedConfCalc)
    },
    async postDeal() {
      if (!this.result) return

      const deal = {
        status: 3,
        deal_status_ready_to_change: true
      }
      await this.$store.dispatch('eggs/postDeal', [this.confCalc.id, deal])
      .finally(async () => setTimeout(this.update, 1000))
      this.result = false
      this.$router.push('/')
    },
    async toggleIsActive() {
      if (confirm('Подтвердите удаление')) {
        const confirmedCalc = {
          model_title: "Подтвержденный просчет",
          model_id: this.confCalc.id
        }
        await this.$store.dispatch('eggs/toggleIsActive', confirmedCalc)
        .finally(async () => setTimeout(this.update, 1000))
          this.$router.push('/')
      }
    },
    update() {
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
    },
    paymentType() {
      switch (this.confCalc.delivery_type_of_payment) {
        case 20:
          return 'С НДС'
        case 0:
          return 'Без НДС'
      }
    }
  },
  computed: {
    confCalc() {
      return this.$store.state.eggs.currentConfCalculate
    },
    postponementPayForUs() {
      let day
      if (this.confCalc.postponement_pay_for_us == 1) {
        day = 'день'
      }
      else if (this.confCalc.postponement_pay_for_us >= 2 && this.confCalc.postponement_pay_for_us <= 4) {
        day = 'дня'
      }
      else if (this.confCalc.postponement_pay_for_us > 4) {
        day = 'дней'
      }
      else {
        return 'Отсутствует'
      }
      const postponement = `${this.confCalc.postponement_pay_for_us} ${day}`
      return postponement
    },
    postponementPayForBuyer() {
      let day
      if (this.confCalc.postponement_pay_for_buyer == 1) {
        day = 'день'
      }
      else if (this.confCalc.postponement_pay_for_buyer >= 2 && this.confCalc.postponement_pay_for_buyer <= 4) {
        day = 'дня'
      }
      else if (this.confCalc.postponement_pay_for_buyer > 4) {
        day = 'дней'
      }
      else {
        return 'Отсутствует'
      }
      const postponement = `${this.confCalc.postponement_pay_for_buyer} ${day}`
      return postponement
    }
  },
}
</script>

<style lang="scss" scoped>
.card {
  width: 100%;
  float: left;
  background-color: #f9f9f9;

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
  &__button-wrapper{
    display: flex;
    justify-content: center;
    border-radius: 10px;
    padding: 2px 5px;
    gap: 5px;
    background-color: #fff;
    border: solid 2px #f3f3f3;
  }
}

.conf-calculate {
  display: flex;

  &__title {
    width: 100%;
    height: 40px;
    font-size: 20px;
    font-weight: 600;
    color: #7b7b7b;
    margin: 0 auto;
    justify-content: center;
    align-items: center;
    border: solid 2px #f3f3f3;
    border-bottom: 0;
    border-radius: 10px;
    background-color: #fff;
  }
  &__container {
    flex-direction: column;
    flex-flow: column;
    justify-content: center;
    align-items: center;
    background-color: #fff;
    border: solid 2px #f3f3f3;
    border-radius: 10px;
    padding: 7px 5px;
    margin-bottom: 5px;
  }
  &__row {
    display: inline-flex;
    flex-flow: row;
    width: 100%;
    margin-bottom: 5px;
    gap: 5px;
    align-items: center;
  }
  &__attr {
    color: #c4c4c4;
    font-size: 16px;
    margin-bottom: 4px;
  }
  &__scroll {
    display: inline;
    overflow-y: scroll;
    height: 28px;
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
    margin-right: 5px;
  }
  &__info-scroll {
    display: inline;
    height: 28px;
  }
  &__item {
    display: inline;
    height: 28px;
    width: 50%;
    border-bottom: solid 1.5px;
  }
  &__seller {
    padding-left: 10px;
    border-color: #00a2ff4b;
    border-radius: 0 0 0 5px;
  }
  &__buyer {
    text-align: end;
    padding-right: 10px;
    border-color: #48ff004b;
    border-radius: 0 0 5px 0;
  }
}

.scroll {
  overflow-y: scroll;
}

@media (min-width: 1600px) {
  .conf-calculate__title {
    font-size: 20px;
  }
  .conf-calculate__attr {
    font-size: 16px;
  }
  .ca-name {
    font-size: 15px;
  }
}

@media (min-width: 1200px) and (max-width: 1599px) {
  .conf-calculate__title {
    font-size: 18px;
  }
  .conf-calculate__attr {
    font-size: 14px;
  }
  .ca-name {
    font-size: 13px;
  }
}

.ca {
  &:hover {
    cursor: pointer;
    color: #1e6ac8e8;
  }
}

.ca-name {
  width: 30%; 
  font-size: 15px;
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

.addButton {
  display: flex;
  margin-bottom: 1vh;
  width: 39vw;
}

.border {
  height: 40px;
  padding-top: 7px;
  border: solid #f8f8f8 2px;
  border-radius: 5px;
  background-color: #f5f5f5;
}

.border-title {
  // cursor: pointer;
  height: 40px;
  padding-top: 7px;
  border: solid #f8f8f8 2px;
  border-radius: 5px;
  background-color: #ff7b0015;
}

.border-seller {
  height: 40px;
  cursor: pointer;
  padding-top: 7px;
  margin-top: 1.5rem;
  border: solid #f8f8f8 2px;
  border-radius: 5px;
  background-color: #00a2ff15;
}

.border-buyer {
  height: 40px;
  cursor: pointer;
  padding-top: 7px;
  border: solid #f8f8f8 2px;
  border-radius: 5px;
  background-color: #48ff0015;
}

.logist {
  cursor: pointer;
  background-color: #2000af15;
}

.trader-info {
  cursor: pointer;
  &:hover {
      background-color: #f5f5f5;
    }
}

.app-type {
  font-size: 14px;
  width: 100%;
  text-align: center;
  padding: 0;
  margin-bottom: 0.2vh;
  border: solid 1px #ebebeb;
  border-radius: 5px;

  &__import {
    background-color: #c411dc3f;
  }
  &__advance {
    background-color: #a9680d4f;
  }
  &__on-credit {
    background-color: #9e9e9e45;
  }
}
</style>
  
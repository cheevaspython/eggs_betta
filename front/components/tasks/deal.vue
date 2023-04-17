<template>
  <div>
    <div class="card box" style="width: 40vw" v-if="currentDeal">
      <div style="background-color: #fff; border-radius: 10px; margin-bottom: 5px">
        <h4 class="title has-text-centered border-title" style="margin-bottom: 0" @click="showDeal = !showDeal">{{ `Сделка №${currentDeal.id}` }}</h4>
      </div>

      <div class="status-bar">
        <div class="status-bar__status" 
          title-text="Ожидает подтверждения фин. директора"
          v-bind:style="{ 'background-color': getStatusColor(1) }">1</div>
        <div class="status-bar__status" 
          title-text="Ожидание загрузки документов, основание для платежа продавцу"
          v-bind:style="{ 'background-color': getStatusColor(2) }">2</div>
        <div class="status-bar__status" 
          title-text="В процессе подтверждения на оплату продавцу"
          v-bind:style="{ 'background-color': getStatusColor(3) }">3</div>
        <div class="status-bar__status" 
          title-text="В процессе оплаты и загрузки бухгалтером счета от продавца"
          v-bind:style="{ 'background-color': getStatusColor(4) }">4</div>
        <div class="status-bar__status" 
          title-text="На контроле погрузки товара, ожидаем загрузку УПД"
          v-bind:style="{ 'background-color': getStatusColor(5) }">5</div>
        <div class="status-bar__status" 
          title-text="Товар в пути, ожидаем запрос исходящей УПД"
          v-bind:style="{ 'background-color': getStatusColor(6) }">6</div>
        <div class="status-bar__status" 
          title-text="Ожидание загрузки бухгалтером исходящей УПД"
          v-bind:style="{ 'background-color': getStatusColor(7) }">7</div>
        <div class="status-bar__status" 
          title-text="На контроле разгрузки, в ожидании подписанной УПД"
          v-bind:style="{ 'background-color': getStatusColor(8) }">8</div>
          <div class="status-bar__status" 
          title-text="На ожидании закрывающих документов"
          v-bind:style="{ 'background-color': getStatusColor(9) }">9</div>
      </div>

      <div class="deal deal__container">
        <div class="deal__info">
          <div class="deal__info-name">Статус</div>
          <div class="scroll" style="text-align: end;">{{ status }}</div>
        </div>
      </div>

      <div class="deal deal__title">Продукция</div>
      <CalcTable :calc="currentDeal"/>

      <div class="deal deal__container">
        <div class="deal__info ca" @click="showExpenseInfo()" v-show="currentUserRole != 4">
          <div class="deal__info-name">Доп. расход</div>
          <div>{{ currentDeal.expense_total || 0 }} ₽</div>
        </div>
        <div class="deal__info" v-show="currentUserRole != 4">
          <div class="deal__info-name">Маржа</div>
          <div>{{ currentDeal.margin || 0 }} ₽</div>
        </div>
        <div class="deal__info" v-show="currentDeal.cash">
          <div class="deal__info-name">Продажа</div>
          <div>За наличные</div>
        </div>
        <div class="deal__info" v-show="currentDeal.payback_day_for_us">
          <div class="deal__info-name">Дата оплаты продавцу</div>
          <div>{{ getStrDay(currentDeal.payback_day_for_us) }}</div>
        </div>
        <div class="deal__info" v-show="currentDeal.payback_day_for_buyer">
          <div class="deal__info-name">Дата оплаты покупателем</div>
          <div>{{ getStrDay(currentDeal.payback_day_for_buyer) }}</div>
        </div>
      </div>

      <div class="deal deal__title" v-show="!currentDeal.delivery_by_seller">Логист</div>
      <div class="deal deal__container" v-show="!currentDeal.delivery_by_seller">
        <div class="deal__info ca" @click="showLogicInfo(currentDeal.current_logic)">
          <div class="deal__info-name">Название</div>
          <div class="scroll">{{ currentDeal.logic_name }}</div>
        </div>
        <div class="deal__info">
          <div class="deal__info-name">ИНН</div>
          <div>{{ currentDeal.logic_inn }}</div>
        </div>
        <div class="deal__info" v-if="currentDeal.delivery_by_seller">
          <div class="deal__info-name">Доставка</div>
          <div>От продавца</div>
        </div>
        <div v-else style="width: 100%;">
          <div class="deal__info">
            <div class="deal__info-name">Стоимость доставки</div>
            <div>{{ currentDeal.delivery_cost || 0 }} ₽</div>
          </div>
          <div class="deal__info">
            <div class="deal__info-name">Тип оплаты доставки</div>
            <div>{{ paymentType() }}</div>
          </div>
        </div>
      </div>

      <div class="deal deal__title">Контрагенты</div>
      <div class="deal deal__container">
        <div class="deal__attr" style="display: inline-flex; justify-content: space-between; width: 100%; padding: 0 10px;">
          <div class="ca-name" style="text-align: start;">Продавец</div>
          <div>Название</div>
          <div class="ca-name" style="text-align: end;">Покупатель</div>
        </div>
        <div class="deal__row">
          <div class="deal__item deal__seller ca scroll" @click="showSellerInfo(currentDeal.seller)">{{ currentDeal.seller_name }}</div>
          <div class="deal__item deal__buyer ca scroll" style="text-align: end;" @click="showBuyerInfo(currentDeal.buyer)">{{ currentDeal.buyer_name }}</div>
        </div>
        <div class="deal__attr">ИНН</div>
        <div class="deal__row">
          <div class="deal__item deal__seller">{{ currentDeal.seller }}</div>
          <div class="deal__item deal__buyer" style="text-align: end;">{{ currentDeal.buyer }}</div>
        </div>
        <div class="deal__attr">Адрес погрузки/разгрузки</div>
        <div class="deal__row">
          <div class="deal__item deal__seller scroll">{{ currentDeal.loading_address }}</div>
          <div class="deal__item deal__buyer scroll" style="text-align: end;">{{ currentDeal.unloading_address }}</div>
        </div>
        <div class="deal__attr">Дата погрузки/разгрузки</div>
        <div class="deal__row">
          <div class="deal__item deal__seller">{{ getStrDay(currentDeal.delivery_date_from_seller) }}</div>
          <div class="deal__item deal__buyer" style="text-align: end;">{{ getStrDay(currentDeal.delivery_date_to_buyer) }}</div>
        </div>
        <div v-show="currentDeal.actual_loading_date || currentDeal.actual_unloading_date" style="width: 100%;">
          <div class="deal__attr">Фактическая дата погрузки/разгрузки</div>
          <div class="deal__row">
            <div class="deal__item deal__seller"><span v-show="currentDeal.actual_loading_date">{{ getStrDay(currentDeal.actual_loading_date) }}</span></div>
            <div class="deal__item deal__buyer" style="text-align: end;"><span v-show="currentDeal.actual_unloading_date">{{ getStrDay(currentDeal.actual_unloading_date) }}</span></div>
          </div>
        </div>
        <div class="deal__attr">Отсрочка оплаты</div>
        <div class="deal__row">
          <div class="deal__item deal__seller">{{ postponementPayForUs }}</div>
          <div class="deal__item deal__buyer" style="text-align: end;">{{ postponementPayForBuyer }}</div>
        </div>
      </div>

      <div class="deal deal__container">
        <div class="deal__info">
          <div class="deal__info-name">Автор</div>
          <div>{{ currentDeal.owner_name }}</div>
        </div>
        <div class="deal__info" v-show="currentDeal.comment">
          <div class="deal__info-name">Комментарий</div>
          <div class="scroll" style="text-align: end;">{{ currentDeal.comment }}</div>
        </div>
      </div>

      <div class="card__button-wrapper">
        <b-button type="is-success" @click="loadDoc" style="margin-right: 5px" v-show="downloadBtn">Загрузить</b-button>
        <b-button type="is-success" @click="factDate" style="margin-right: 5px; padding: 0 5px;" v-show="currentDeal.deal_status == 5 || currentDeal.deal_status == 8">Фактическая дата</b-button>
        <b-button type="is-success" @click="nextDealStatus" style="margin-right: 5px" :disabled="continueBtnDisabled()" v-show="statusAction">{{ statusAction }}</b-button>
        
        <b-dropdown position="is-top-right">
          <template #trigger>
            <b-button label="Действия" type="is-info is-light" icon-right="menu-up" />
          </template>
          <b-dropdown-item style="padding: 0; margin-bottom: 3px;">
            <b-button type="is-success" @click="checkPermission" label="Документы" style="width: 100%;" />
          </b-dropdown-item>
          <b-dropdown-item style="padding: 0; margin-bottom: 3px;">
            <b-button type="is-warning" @click="addExpense" label="Доп. расход" style="width: 100%;" />
          </b-dropdown-item>
          <b-dropdown-item style="padding: 0; margin-bottom: 3px;">
            <b-button type="is-success is-light" @click="editDeal" label="Редактировать" style="width: 100%;" />
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
    <div v-show="showExpense" v-if="currentDeal.expense_detail_json" style="float: right">
      <expense :expenseList="currentDeal.expense_detail_json"/>
    </div>
  </div>
</template>
  
<script>
import VuePdfEmbed from "vue-pdf-embed/dist/vue2-pdf-embed"
import ModalDealUploadForm from '@/components/editForms/ModalDealUploadForm'
import ModalDealEditForm from '@/components/editForms/ModalDealEditForm'
import documents from '@/components/documents'
import addExpense from "@/components/addExpense"
import factDealDates from "@/components/factDealDates"
export default {
  name: 'Deal',
  components: {
    SellerInfo: () => import("@/components/cards/SellerInfo"),
    BuyerInfo: () => import("@/components/cards/BuyerInfo"),
    LogicInfo: () => import("@/components/cards/LogicInfo"),
    VuePdfEmbed,
    expense: () => import("@/components/expense")
  },
  data(){
    return {
      showDeal: true,
      currentSeller: null,
      currentBuyer: null,
      currentLogic: null,
      showBuyerCard: false,
      showSellerCard: false,
      showLogicCard: false,
      showExpense: false,
      documents_detail: null,
      currentUserRole: localStorage.getItem('userRole'),
      token: localStorage.getItem('access_token'),
      headers: {
        Authorization: `Bearer ${this.token}`
      },
    }
  },
  created() {
    if (!this.documents_detail) {
      this.downloadDocs()
    }
    else if (this.currentDeal.documents != this.documents_detail.id) {
      this.downloadDocs()
    }
  },
  beforeUpdate() {
    if (!this.documents_detail) {
      this.downloadDocs()
    }
    else if (this.currentDeal.documents != this.documents_detail.id) {
      this.downloadDocs()
    }
  },
  methods: {
    async downloadDocs() {
      const docs = await this.$store.dispatch('eggs/getDealDocs', this.currentDeal.documents)
      this.documents_detail = docs
    },
    getStatusColor(status) {
      if (this.currentDeal.deal_status > status) {
        return 'hsl(121deg, 77%, 85%)'
      }
      else if (this.currentDeal.deal_status == status) {
        return 'hsl(62deg, 94%, 85%)'
      }
      else {
        return '#fff'
      }
    },
    factDate() {
      this.$buefy.modal.open({
        parent: this,
        component: factDealDates,
        hasModalCard: true,
        trapFocus: true,
        props:{
          deal: this.currentDeal
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
    checkPermission() {
      const acceptedRoles = ['4', '6', '7', '8']
      const dealManagers = [this.currentDeal.seller_manager, this.currentDeal.buyer_manager]
      const userId = Number(localStorage.getItem('userId'))
      if (acceptedRoles.includes(this.currentUserRole)) {
        this.viewDocuments()
      }
      else if (dealManagers.includes(userId)) {
        this.viewDocuments()
      }
      else {
        return alert('Доступ запрещен')
      }
    },
    async viewDocuments() {
      if (this.currentUserRole == '4') {
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
      await this.downloadDocs()
      this.$buefy.modal.open({
        parent: this,
        component: documents,
        hasModalCard: true,
        trapFocus: true,
        props:{
          docs: this.documents_detail
        }
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
    async getSellerByInn(inn) {
      const token = localStorage.getItem('access_token')
      const seller = await this.$axios.get(`eggs/seller_card/${inn}`, {headers: {Authorization: `Bearer ${token}`}})
      this.currentSeller = seller.data
      this.showSellerCard = true
    },
    showSellerInfo(seller_inn) {
      this.showBuyerCard = false
      this.showLogicCard = false
      this.showExpense = false
      if (this.currentSeller) {
        if (seller_inn == this.currentSeller.inn) {
          this.showSellerCard = !this.showSellerCard
        }
        else {
          this.getSellerByInn(seller_inn)
        }
      }
      else {
        this.getSellerByInn(seller_inn)
      }
    },
    async getBuyerByInn(inn) {
      const token = localStorage.getItem('access_token')
      const buyer = await this.$axios.get(`eggs/buyer_card/${inn}`, {headers: {Authorization: `Bearer ${token}`}})
      this.currentBuyer = buyer.data
      this.showBuyerCard = true
    },
    showBuyerInfo(buyer_inn) {
      this.showSellerCard = false
      this.showLogicCard = false
      this.showExpense = false
      if (this.currentBuyer) {
        if (buyer_inn == this.currentBuyer.inn) {
          this.showBuyerCard = !this.showBuyerCard
        }
        else {
          this.getBuyerByInn(buyer_inn)
        }
      }
      else {
        this.getBuyerByInn(buyer_inn)
      }
    },
    async showLogicInfo(logic) {
      this.showBuyerCard = false
      this.showSellerCard = false
      this.showExpense = false
      if (this.currentLogic) {
        this.showLogicCard = !this.showLogicCard
      }
      else {
        this.currentLogic = await this.$store.dispatch('ca/getCurrentLogic', logic)
        this.showLogicCard = true
      }
    },
    showExpenseInfo() {
      if (this.currentDeal.expense_total == 0) return
      this.showBuyerCard = false
      this.showSellerCard = false
      this.showLogicCard = false
      this.showExpense = !this.showExpense
    },
    async nextDealStatus() {
      const result = confirm('Подтвердить?')
      if (!result) {
        return
      }
      await this.$store.dispatch('eggs/patchDealStatus', this.currentDeal.id)
      .finally( () => setTimeout(this.update, 1000))
      const updatedDeal = await this.$store.dispatch('eggs/getModel', this.currentDeal.id)
      await this.$store.dispatch('eggs/setCurrentDeal', updatedDeal)
      this.result = false
      this.$emit('toggle-card')
      this.$router.push('/')
    },
    toggleCard() {
      this.$emit('toggle-card')
    },
    update() {
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
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
          task: this.currentDeal,
          title: `Сделки №${this.currentDeal.id}`
        }
      })
    },
    loadDoc() {
      if (!this.documents_detail) {
        this.downloadDocs()
      }
      else if (this.currentDeal.documents != this.documents_detail.id) {
        this.downloadDocs()
      }
      this.$buefy.modal.open({
        parent: this,
        component: ModalDealUploadForm,
        hasModalCard: true,
        trapFocus: true,
        props:{
          deal: this.currentDeal,
          docs: this.documents_detail
          // 'v-on:toggle-card': this.toggleCard()
        }
      })
    },
    async toggleIsActive() {
      if (confirm('Подтвердите удаление')) {
        const deal = {
          model_id: this.currentDeal.id,
          model_title: "Сделка"
        }
        await this.$store.dispatch('eggs/toggleIsActive', deal)
        .finally( () => setTimeout(this.update, 1000))
        this.toggleCard()
        this.$router.push('/')
      }
    },
    paymentType() {
      switch (this.currentDeal.delivery_type_of_payment) {
        case 20:
          return 'С НДС'
        case 0:
          return 'Без НДС'
      }
    },
    editDeal() {
      if (this.currentUserRole == '4' && this.currentDeal.delivery_by_seller) {
        return alert('Доставка осуществляется продавцом')
      }
      this.$buefy.modal.open({
        parent: this,
        component: ModalDealEditForm,
        hasModalCard: true,
        trapFocus: true,
        props:{
          deal: this.currentDeal
        }
      })
    },
    async checkDownloadByStatus() {
      if (!this.documents_detail) {
        this.downloadDocs()
      }
      else if (this.currentDeal.documents != this.documents_detail.id) {
        this.downloadDocs()
      }
      switch (this.currentDeal.deal_status) {
        case 2:
          if (this.documents_detail.payment_order || this.documents_detail.payment_for_contract) {
            return false
          }
        case 4:
          if (this.documents_detail.account_to_seller) {
            return false
          }
        case 5:
          if (this.documents_detail.UPD_incoming && this.currentDeal.actual_loading_date) {
            return false
          }
        case 7:
          if (this.documents_detail.UPD_outgoing) {
            return false
          }
        case 8:
          if (this.documents_detail.UPD_outgoing && this.currentDeal.actual_unloading_date) {
            return false
          }
        default:
          return true
      }
    },
    continueBtnDisabled() {
      return false
      // switch (this.currentDeal.deal_status) {
      //   case 1:
      //   case 3:
      //   case 6:
      //     return false
      //   default: 
      //     return this.checkDownloadByStatus()
      // }
    }
  },
  computed: {
    currentDeal() {
      return this.$store.state.eggs.currentDeal
    },
    status() {
      switch (this.currentDeal.deal_status) {
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
        case 9:
          return 'На ожидании закрывающих документов'
        default:
          return 'Сделка закрыта'
      }
    },
    statusAction() {
      switch (this.currentDeal.deal_status) {
        case 1:
          return 'Подтвердить'
        case 2:
          return 'Продолжить'
        case 3:
          return 'Подтвердить'
        case 4:
          return 'Продолжить'
        case 5:
          return 'Продолжить'
        case 6:
          return 'Запросить'
        case 7:
          return 'Продолжить'
        case 8:
          return 'Продолжить'
      }
    },
    downloadBtn() {
    //   switch (this.currentDeal.deal_status) {
    //     case 1:
    //       return false
    //     case 2:
    //       return true
    //     case 3:
    //       return false
    //     case 4:
    //       return true
    //     case 5:
    //       return true
    //     case 6:
    //       return false
    //     case 7:
    //       return true
    //     case 8:
    //       return true
    //   }
      return true
    },
    postponementPayForUs() {
      let day
      if (this.currentDeal.postponement_pay_for_us == 1) {
        day = 'день'
      }
      else if (this.currentDeal.postponement_pay_for_us >= 2 && this.currentDeal.postponement_pay_for_us <= 4) {
        day = 'дня'
      }
      else if (this.currentDeal.postponement_pay_for_us > 4) {
        day = 'дней'
      }
      else {
        return 'Отсутствует'
      }
      const postponement = `${this.currentDeal.postponement_pay_for_us} ${day}`
      return postponement
    },
    postponementPayForBuyer() {
      let day
      if (this.currentDeal.postponement_pay_for_buyer == 1) {
        day = 'день'
      }
      else if (this.currentDeal.postponement_pay_for_buyer >= 2 && this.currentDeal.postponement_pay_for_buyer <= 4) {
        day = 'дня'
      }
      else if (this.currentDeal.postponement_pay_for_buyer > 4) {
        day = 'дней'
      }
      else {
        return 'Отсутствует'
      }
      const postponement = `${this.currentDeal.postponement_pay_for_buyer} ${day}`
      return postponement
    }
  }
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

.deal {
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
    text-align: center;
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

@media (min-width: 1600px) {
  .status-bar__status {
    font-size: 16px;
  }
}

@media (min-width: 1200px) and (max-width: 1599px) {
  .status-bar__status {
    font-size: 14px;
  }
}

.status-bar {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  height: 20px;
  width: 100%;
  margin-bottom: 5px;
  
  &__status {
    height: 100%;
    width: 12.5%;
    cursor: pointer;
    border: solid 2px #ebebeb;
    border-radius: 5px 25px 5px 25px;
    background-color: #fff;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.8s 0.5s;

    &:hover {
      width: 14%;
      border-color: #9a9a9a;
    }
  }
}

.status-bar__status:hover::after {
  position: absolute;
  top: -20px;
  width: 50%;
  z-index: 100;
  transition: transform 250ms;
  transition-timing-function: linear;
  background-color: #fff;
  border: solid 2px #ebebeb;
  outline: solid 1px #9a9a9a;
  border-radius: 10px;
  padding: 10px 20px;
  text-align: center;
  content: attr(title-text);
}

.scroll {
  overflow-y: scroll;
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

.border {
  height: 40px;
  padding-top: 7px;
  border: solid #f8f8f8 2px;
  border-radius: 5px;
  background-color: #f5f5f5;
}

.border-title {
  cursor: pointer;
  height: 40px;
  padding-top: 7px;
  border: solid #f8f8f8 2px;
  border-radius: 5px;
  background-color: #ff110015;
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

.seller-section {
  // border: solid 2px #099cf115;
  // border-right: solid 2px #f5f5f5;
  margin-bottom: 10px;
  background-color: #099cf110;
}

.buyer-section {
  // border: solid 2px #4ce21115;
  // border-right: solid 2px #f5f5f5;
  margin-bottom: 10px;
  background-color: #4ce21110;
}
</style>
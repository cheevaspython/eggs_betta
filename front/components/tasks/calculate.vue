<template>
  <div>
    <div class="card box" style="width: 40vw" v-if="calc">
      <div style="background-color: #fff; border-radius: 10px;">
        <h4 class="title has-text-centered border-title">{{ `Просчет №${calc.id}` }}</h4>
      </div>
        
      <div class="calculate calculate__title">Продукция</div>
      
      <CalcTable :calc="calc" />
        
      <div class="calculate__container">
        <div class="calculate__info" v-if="calc.delivery_by_seller">
          <div class="calculate__info-name">Доставка</div>
          <div>От продавца</div>
        </div>
        <div v-else>
          <div class="calculate__info">
            <div class="calculate__info-name">Приблизительная стоимость доставки</div>
            <div>{{ calc.delivery_cost || 0 }} ₽</div>
          </div>
          <div class="calculate__info">
            <div class="calculate__info-name">Тип оплаты доставки</div>
            <div>{{ paymentType() || '-' }}</div>
          </div>
        </div>
        <div class="calculate__info">
          <div class="calculate__info-name">Маржа</div>
          <div>{{ calc.margin || 0 }} ₽</div>
        </div>
        <div class="calculate__info" v-show="calc.cash">
          <div class="calculate__info-name">Продажа</div>
          <div>За наличные</div>
        </div>
      </div>
      
      <div class="calculate calculate__title">Контрагенты</div>
      <div class="calculate calculate__container">
        <div class="calculate__attr" style="display: inline-flex; justify-content: space-between; width: 100%; padding: 0 10px;">
          <div class="ca-name">Продавец</div>
          <div>Название</div>
          <div class="ca-name" style="text-align: end;">Покупатель</div>
        </div>
        <div class="calculate__row">
          <div class="calculate__item calculate__seller ca scroll" @click="showSellerInfo(calc.seller)">{{ calc.seller_name }}</div>
          <div class="calculate__item calculate__buyer ca scroll" style="text-align: end;" @click="showBuyerInfo(calc.buyer)">{{ calc.buyer_name }}</div>
        </div>
        <div class="calculate__attr">ИНН</div>
        <div class="calculate__row">
          <div class="calculate__item calculate__seller">{{ calc.seller }}</div>
          <div class="calculate__item calculate__buyer" style="text-align: end;">{{ calc.buyer }}</div>
        </div>
        <div class="calculate__attr">Адрес погрузки/разгрузки</div>
        <div class="calculate__row">
          <div class="calculate__item calculate__seller scroll">{{ calc.loading_address }}</div>
          <div class="calculate__item calculate__buyer scroll" style="text-align: end;">{{ calc.unloading_address }}</div>
        </div>
        <div class="calculate__attr">Дата погрузки/разгрузки</div>
        <div class="calculate__row">
          <div class="calculate__item calculate__seller">{{ getStrDay(calc.delivery_date_from_seller) }}</div>
          <div class="calculate__item calculate__buyer" style="text-align: end;">{{ getStrDay(calc.delivery_date_to_buyer) }}</div>
        </div>
        <div class="calculate__attr">Отсрочка оплаты</div>
        <div class="calculate__row">
          <div class="calculate__item calculate__seller">{{ postponementPayForUs }}</div>
          <div class="calculate__item calculate__buyer" style="text-align: end;">{{ postponementPayForBuyer }}</div>
        </div>
      </div>
      
      <div class="calculate__container">
        <div class="calculate__info" v-show="calc.comment">
          <div class="calculate__info-name">Комментарий</div>
          <div class="calculate__info-scroll" style="text-align: end;">{{ calc.comment || '-' }}</div>
        </div>
        <div class="calculate__info">
          <div class="calculate__info-name">Автор</div>
          <div>{{ calc.owner_name }}</div>
        </div>
      </div>

      <div class="card__button-wrapper">
        <b-button type="is-success" @click="makeConfCalcOrder">Подтвердить просчет</b-button>
        <b-dropdown position="is-top-right">
          <template #trigger>
            <b-button label="Действия" type="is-info is-light" icon-right="menu-up" />
          </template>
          <b-dropdown-item style="padding: 0; margin-bottom: 3px;">
            <b-button type="is-warning" @click="makeNote" label="Замечание" style="width: 100%;" />
          </b-dropdown-item>
          <b-dropdown-item style="padding: 0; margin-bottom: 3px;">
            <b-button type="is-success is-light" @click="editCalculate" label="Редактировать" style="width: 100%;" />
          </b-dropdown-item>
          <b-dropdown-item style="padding: 0; margin-bottom: 3px;">
            <b-button type="is-danger is-light" @click="toggleIsActive" label="Удалить" style="width: 100%;" v-show="canDelete()" />
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
  </div>
</template>
  
<script>
import ModalCalcEditForm from '@/components/editForms/ModalCalcEditForm'
import note from '@/components/note'
export default {
  name: 'Calculate',
  components: {
    SellerInfo: () => import("@/components/cards/SellerInfo"),
    BuyerInfo: () => import("@/components/cards/BuyerInfo"),
    CalcTable: () => import("@/components/CalcTable")
  },
  data() {
    return {
      currentSeller: null,
      currentBuyer: null,
      showCalc: true,
      showSeller: true,
      showBuyer: true,
      showSellerCard: false,
      showBuyerCard: false,
    }
  },
  methods: {
    canDelete() {
      const acceptedRoles = ['6', '8']
      if (!acceptedRoles.includes(this.currentUserRole)) {
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
    makeNote() {
      this.$buefy.modal.open({
        parent: this,
        component: note,
        hasModalCard: true,
        trapFocus: true,
        props:{
          task: this.calc,
          title: 'Просчету'
        }
      })
    },
    getStrDay(dateStr) {
      const date = Date.parse(dateStr)
      const currentDate = new Date(date)
      return currentDate.getDate() + ' ' + this.getStrMonth(currentDate.getMonth()) + ' ' + currentDate.getFullYear()
    },
    async makeConfCalcOrder() {
      const result = confirm('Подтвердить просчет?')
      if (!result) {
        return
      }
      const confCalc = {
        status: 2
      }
      await this.$store.dispatch('eggs/postConfCalc', [confCalc, this.calc.id])
      .finally( () => setTimeout(this.update, 1000))
      await this.$router.push('/')
    },
    update() {
      this.$store.dispatch('bid/getOwnerTasks')
    },
    editCalculate() {
      const calculate = this.calc
      this.$buefy.modal.open({
        parent: this,
        component: ModalCalcEditForm,
        hasModalCard: true,
        trapFocus: true,
        props:{
          calculate: calculate
        }
      })
    },
    async showSellerInfo(seller_inn) {
      const token = localStorage.getItem('access_token')
      const seller = await this.$axios.get(`eggs/seller_card/${seller_inn}/`, {headers: {Authorization: `Bearer ${token}`}})
      this.currentSeller = seller.data
      this.showBuyerCard = false
      if (this.currentSeller.inn == seller.data.inn) {
        this.showSellerCard = !this.showSellerCard
      }
      else {
        this.currentSeller = seller.data, 
        this.showSellerCard = true
      }
    },
    async showBuyerInfo(buyer_inn) {
      const token = localStorage.getItem('access_token')
      const buyer = await this.$axios.get(`eggs/buyer_card/${buyer_inn}/`, {headers: {Authorization: `Bearer ${token}`}})
      this.currentBuyer = buyer.data
      this.showSellerCard = false
      if (this.currentBuyer.inn == buyer.data.inn) {
        this.showBuyerCard = !this.showBuyerCard
      }
      else {
        this.currentBuyer = buyer.data, 
        this.showBuyerCard = true
      }
    },
    async toggleIsActive() {
      if (confirm('Подтвердите удаление')) {
        const calculate = {
          model_title: "Просчет",
          model_id: this.calc.id
        }
        await this.$store.dispatch('eggs/toggleIsActive', calculate)
        .finally(async () => 
          await this.$store.dispatch('bid/getOwnerTasks'),
          this.$store.dispatch('user/getUserNotifications')
        )
        this.$router.push('/')
      }
    },
    paymentType() {
      switch (this.calc.delivery_type_of_payment) {
        case 20:
          return 'С НДС'
        case 0:
          return 'Без НДС'
      }
    },
  },
  computed: {
    calc() {
      return this.$store.state.eggs.currentCalculate
    },
    postponementPayForUs() {
      let day
      if (this.calc.postponement_pay_for_us == 1) {
        day = 'день'
      }
      else if (this.calc.postponement_pay_for_us >= 2 && this.calc.postponement_pay_for_us <= 4) {
        day = 'дня'
      }
      else if (this.calc.postponement_pay_for_us > 4) {
        day = 'дней'
      }
      else {
        return 'Отсутствует'
      }
      const postponement = `${this.calc.postponement_pay_for_us} ${day}`
      return postponement
    },
    postponementPayForBuyer() {
      let day
      if (this.calc.postponement_pay_for_buyer == 1) {
        day = 'день'
      }
      else if (this.calc.postponement_pay_for_buyer >= 2 && this.calc.postponement_pay_for_buyer <= 4) {
        day = 'дня'
      }
      else if (this.calc.postponement_pay_for_buyer > 4) {
        day = 'дней'
      }
      else {
        return 'Отсутствует'
      }
      const postponement = `${this.calc.postponement_pay_for_buyer} ${day}`
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

.calculate {
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
    overflow-y: scroll;
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
  .calculate__title {
    font-size: 20px;
  }
  .calculate__attr {
    font-size: 16px;
  }
  .ca-name {
    font-size: 15px;
  }
}

@media (min-width: 1200px) and (max-width: 1599px) {
  .calculate__title {
    font-size: 18px;
  }
  .calculate__attr {
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

.border {
  height: 40px;
  padding-top: 7px;
  border: solid #f8f8f8 2px;
  border-radius: 5px;
  background-color: #f5f5f5;
}

.border-title {
  // cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  margin-bottom: 10px;
  // padding-top: 7px;
  border: solid #f3f3f3 2px;
  border-radius: 10px;
  background-color: #ffee0015;
  // background-color: #d4c60015;
}

.border-seller {
  height: 40px;
  cursor: pointer;
  padding-top: 7px;
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

.bottom-border-grey {
  border-bottom: solid #dddddd 2px;
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
  border-radius: 20px;

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
  
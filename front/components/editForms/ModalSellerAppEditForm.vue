<template>
  <form action="" style="width: 1000px">
    <div class="modal-card" style="width: 900px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900; ">Редактирование заявки от продавца №{{applicationFromSeller.id}}</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>

      <section class="modal-card-body is-fullwidth">
        <div class="card__title">Продавец: {{ `${current_seller.name} / ${current_seller.inn}` }}</div>
        <div class="flexbox__row" style="width: 860px">
          <div class="flexbox__row flexbox__space-between input-border">
          <div style="width: calc(35% - 10px); margin-left: 10px">CB кол-во</div>
            <b-field class="my-b-input">
              <b-input placeholder="Введите количество" rounded v-model="cB"></b-input>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin-left: 10px">Стоимость за десяток</div>
            <b-field class="my-b-input-cost">
              <b-input placeholder="Введите сумму" rounded v-model="cB_cost"></b-input>
            </b-field>
          </div>
        </div>

        <div class="flexbox__row" style="width: 860px">
          <div class="flexbox__row flexbox__space-between input-border">
          <div style="width: calc(35% - 10px); margin-left: 10px">C0 кол-во</div>
            <b-field class="my-b-input">
              <b-input placeholder="Введите количество" rounded v-model="c0"></b-input>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin-left: 10px">Стоимость за десяток</div>
            <b-field class="my-b-input-cost">
              <b-input placeholder="Введите сумму" rounded v-model="c0_cost"></b-input>
            </b-field>
          </div>
        </div>

        <div class="flexbox__row" style="width: 860px">
          <div class="flexbox__row flexbox__space-between input-border">
          <div style="width: calc(35% - 10px); margin-left: 10px">C1 кол-во</div>
            <b-field class="my-b-input">
              <b-input placeholder="Введите количество" rounded v-model="c1"></b-input>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin-left: 10px">Стоимость за десяток</div>
            <b-field class="my-b-input-cost">
              <b-input placeholder="Введите сумму" rounded v-model="c1_cost"></b-input>
            </b-field>
          </div>
        </div>

        <div class="flexbox__row" style="width: 860px">
          <div class="flexbox__row flexbox__space-between input-border">
          <div style="width: calc(35% - 10px); margin-left: 10px">C2 кол-во</div>
            <b-field class="my-b-input">
              <b-input placeholder="Введите количество" rounded v-model="c2"></b-input>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin-left: 10px">Стоимость за десяток</div>
            <b-field class="my-b-input-cost">
              <b-input placeholder="Введите сумму" rounded v-model="c2_cost"></b-input>
            </b-field>
          </div>
        </div>

        <div class="flexbox__row" style="width: 860px">
          <div class="flexbox__row flexbox__space-between input-border">
          <div style="width: calc(35% - 10px); margin-left: 10px">C3 кол-во</div>
            <b-field class="my-b-input">
              <b-input placeholder="Введите количество" rounded v-model="c3"></b-input>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin-left: 10px">Стоимость за десяток</div>
            <b-field class="my-b-input-cost">
              <b-input placeholder="Введите сумму" rounded v-model="c3_cost"></b-input>
            </b-field>
          </div>
        </div>

        <div class="flexbox__row" style="width: 860px">
          <div class="flexbox__row flexbox__space-between input-border">
          <div style="width: calc(35% - 10px); margin-left: 10px">Грязь кол-во</div>
            <b-field class="my-b-input">
              <b-input placeholder="Введите количество" rounded v-model="dirt"></b-input>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin-left: 10px">Стоимость за десяток</div>
            <b-field class="my-b-input-cost">
              <b-input placeholder="Введите сумму" rounded v-model="dirt_cost"></b-input>
            </b-field>
          </div>
        </div>

        <div class="flexbox flexbox__row flexbox__space-between input-border" style="height: 450px; width: 100%;">
          <div class="flexbox__column" style=" padding: 10px 20px;">
            <div class="changeDates">Изменение окна поставки</div>
            <div class="flexbox__row flexbox__space-between" style="margin-top: 15px">
              <b-datepicker
                style="width: 360px;"
                v-model="newDates"
                inline
                range>
              </b-datepicker>
            </div>
          </div>
          <div class="flexbox__column" style="border-left: solid 2px #ebebeb;  padding: 10px 20px; height: 100%;">
            <div class="flexbox__column" style="margin: 0 auto; width: 250px;">
              <b-dropdown :triggers="['hover']" aria-role="list">
                <template #trigger>
                  <b-button
                    v-model="loading_address"  
                    label="Изменение адреса погрузки"
                    type="is-success is-light"
                    icon-right="menu-down" 
                    rounded />
                </template>
                  
                <b-dropdown-item v-if="productionAddress1" aria-role="listitem" @click="selectLoadingAddress(productionAddress1)">
                  <strong>{{ productionAddress1 }}</strong></b-dropdown-item>
                <b-dropdown-item v-if="productionAddress2" aria-role="listitem" @click="selectLoadingAddress(productionAddress2)">
                  <strong>{{ productionAddress2 }}</strong></b-dropdown-item>
                <b-dropdown-item v-if="productionAddress3" aria-role="listitem" @click="selectLoadingAddress(productionAddress3)">
                  <strong>{{ productionAddress3 }}</strong></b-dropdown-item>
                <b-dropdown-item v-if="productionAddress4" aria-role="listitem" @click="selectLoadingAddress(productionAddress4)">
                  <strong>{{ productionAddress4 }}</strong></b-dropdown-item>
                <b-dropdown-item v-if="productionAddress5" aria-role="listitem" @click="selectLoadingAddress(productionAddress5)">
                  <strong>{{ productionAddress5 }}</strong></b-dropdown-item>
              </b-dropdown>
            </div>
            <div class="prod-address">
              {{ loading_address }}
            </div>
            <div class="flexbox__row flexbox__space-between input-border" style="width: 100%;">
              <div style="margin-left: 10px">Отсрочка оплаты (дней):</div>
              <b-field class="my-b-input-cost" style="width: 40%;">
                <b-input placeholder="Введите кол-во дней" rounded v-model="postponementPay"></b-input>
              </b-field>
            </div>
          </div>
        </div>

        Комментарий:
        <b-field>
          <b-input v-model="comment" type="textarea" maxlength="255"></b-input>
        </b-field>
      </section>

      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Подтвердить изменения"
          :loading="loading"
          type="is-success"
          @click="sendSellerOrder"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
export default {
  name: "ModalSellerAppEditForm",
  props: ['applicationFromSeller'],
  data() {
    return {
      loading: false,
      isPublic: true,
      updateDates: false,
      current_seller: this.applicationFromSeller.seller_card_detail,
      cB: this.applicationFromSeller.cB,
      cB_cost: this.applicationFromSeller.cB_cost,
      c0: this.applicationFromSeller.c0,
      c0_cost: this.applicationFromSeller.c0_cost,
      c1: this.applicationFromSeller.c1,
      c1_cost: this.applicationFromSeller.c1_cost,
      c2: this.applicationFromSeller.c2,
      c2_cost: this.applicationFromSeller.c2_cost,
      c3: this.applicationFromSeller.c3,
      c3_cost: this.applicationFromSeller.c3_cost,
      dirt: this.applicationFromSeller.dirt,
      dirt_cost: this.applicationFromSeller.dirt_cost,
      productionAddress1: this.applicationFromSeller.seller_card_detail.prod_address_1,
      productionAddress2: this.applicationFromSeller.seller_card_detail.prod_address_2,
      productionAddress3: this.applicationFromSeller.seller_card_detail.prod_address_3,
      productionAddress4: this.applicationFromSeller.seller_card_detail.prod_address_4,
      productionAddress5: this.applicationFromSeller.seller_card_detail.prod_address_5,
      loading_address: this.applicationFromSeller.loading_address,
      dates: [this.applicationFromSeller.delivery_window_from, this.applicationFromSeller.delivery_window_until],
      comment: this.applicationFromSeller.comment,
      postponementPay: this.applicationFromSeller.postponement_pay,
      newDates: [],
    }
  },
  methods: {
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
    removeRow() {
      this.selectedCategories.pop()
    },
    selectLoadingAddress(address){
      this.loading_address = address
    },
    checkDeliveryFrom(dates){
      if (this.newDates.length > 0) {
        return dates[0].getDate() + '.' + (dates[0].getMonth() + 1) + '.' + dates[0].getFullYear()
      }
      else {
        return this.applicationFromSeller.delivery_window_from
      }
    },
    checkDeliveryUntil(dates) {
      if (this.newDates.length > 0) {
        return dates[1].getDate() + '.' + (dates[1].getMonth() + 1) + '.' + dates[1].getFullYear()
      }
      else {
        return this.applicationFromSeller.delivery_window_until
      }
    },
    checkForComma(eggsCost) {
      let eggCost = `${eggsCost}`
      if (eggCost.includes(',')) {
        eggCost = eggCost.replace(',', '.')
      }
      return parseFloat(eggCost)
    },
    async sendSellerOrder() {
      const data = {
        cB: this.cB,
        cB_cost: this.cB_cost ? this.checkForComma(this.cB_cost) : 0,
        c0: this.c0,
        c0_cost: this.c0_cost ? this.checkForComma(this.c0_cost) : 0,
        c1: this.c1,
        c1_cost: this.c1_cost ? this.checkForComma(this.c1_cost) : 0,
        c2: this.c2,
        c2_cost: this.c2_cost ? this.checkForComma(this.c2_cost) : 0,
        c3: this.c3,
        c3_cost: this.c3_cost ? this.checkForComma(this.c3_cost) : 0,
        dirt: this.dirt,
        dirt_cost: this.dirt_cost ? this.checkForComma(this.dirt_cost) : 0,
        loading_address: this.loading_address,
        delivery_window_from: this.checkDeliveryFrom(this.newDates),
        delivery_window_until: this.checkDeliveryUntil(this.newDates),
        postponement_pay: this.postponementPay,
        comment: this.comment
      }
      this.loading = true
      const id = this.applicationFromSeller.id
      const success = await this.$store.dispatch('eggs/patchSellerApp', [data, id])
        .finally(() => this.loading = false, setTimeout(this.update, 1000))
      if (!success) return
      const updatedSellerApp = await this.$store.dispatch('eggs/getSellerApp', id)
      await this.$store.dispatch('eggs/setCurrentAppFromSeller', updatedSellerApp)
      this.$emit('close')
    },
    update() {
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
    },
    clearFromDateTime() {
      this.dateFrom = null
    }
  },
}
</script>

<style lang="scss" scoped>
form {
  font-family: 'Montserrat';
}

.card {
  width: 100%;

  &__title {
    font-size: 22px;
    width: 100%;
    color: #5b5b5b;
    text-align: center;
    font-weight: 600;
    padding: 10px;
    border: 1px solid #dcdcdc;
    border-radius: 40px;
    background-color: #e0f3ff;
    margin-bottom: 15px;
  }
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

.input-border {
  border: solid 2px #ebebeb;
  border-radius: 20px;
  width: 50%;
  height: 40px;
  margin-bottom: 5px;
  align-items: center;
}

.my-b-input {
  width: 65%;
}

.my-b-input-cost {
  width: 50%;
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

.categories__calendar {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
  padding-bottom: 20px;
}

.changeDates {
  display: flex;
  color: white;
  justify-content: center;
  font-size: 18px;
  border-radius: 15px;
  background-color: #823bf570;
}

.prod-address {
  width: 100%;
  height: 26px;
  padding-bottom: 0px; 
  margin-top: 10px;
  margin-bottom: 10px; 
  text-align: center;
  background-color: #f5f5f5;
  border: solid 2px #ebebeb;
  border-top: 0;
  border-radius: 10px;
}
</style>

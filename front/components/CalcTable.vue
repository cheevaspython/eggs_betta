<template>
  <div class="calc-table">
    <div class="calc-table__row">
      <div class="calc-table__cell calc-table__text">Категория</div>
      <div class="calc-table__cell calc-table__text">Кол-во (дес.)</div>
      <div class="calc-table__cell calc-table__text" v-show="currentUserRole != 4">Закупка</div>
      <div class="calc-table__cell calc-table__text" v-show="currentUserRole != 4">Продажа</div>
    </div>
    <div class="calc-table__row line-hover" v-show="calc.cB">
      <div class="calc-table__cell">CB</div>
      <div class="calc-table__cell">{{ calc.cB }}</div>
      <div class="calc-table__cell" v-show="currentUserRole != 4">{{ calc.seller_cB_cost }} ₽</div>
      <div class="calc-table__cell" v-show="currentUserRole != 4">{{ calc.buyer_cB_cost }} ₽</div>
    </div>
    <div class="calc-table__row line-hover" v-show="calc.c0">
      <div class="calc-table__cell">C0</div>
      <div class="calc-table__cell">{{ calc.c0 }}</div>
      <div class="calc-table__cell" v-show="currentUserRole != 4">{{ calc.seller_c0_cost }} ₽</div>
      <div class="calc-table__cell" v-show="currentUserRole != 4">{{ calc.buyer_c0_cost }} ₽</div>
    </div>
    <div class="calc-table__row line-hover" v-show="calc.c1">
      <div class="calc-table__cell">C1</div>
      <div class="calc-table__cell">{{ calc.c1 }}</div>
      <div class="calc-table__cell" v-show="currentUserRole != 4">{{ calc.seller_c1_cost }} ₽</div>
      <div class="calc-table__cell" v-show="currentUserRole != 4">{{ calc.buyer_c1_cost }} ₽</div>
    </div>
    <div class="calc-table__row line-hover" v-show="calc.c2">
      <div class="calc-table__cell">C2</div>
      <div class="calc-table__cell">{{ calc.c2 }}</div>
      <div class="calc-table__cell" v-show="currentUserRole != 4">{{ calc.seller_c2_cost }} ₽</div>
      <div class="calc-table__cell" v-show="currentUserRole != 4">{{ calc.buyer_c2_cost }} ₽</div>
    </div>
    <div class="calc-table__row line-hover" v-show="calc.c3">
      <div class="calc-table__cell">C3</div>
      <div class="calc-table__cell">{{ calc.c3 }}</div>
      <div class="calc-table__cell" v-show="currentUserRole != 4">{{ calc.seller_c3_cost }} ₽</div>
      <div class="calc-table__cell" v-show="currentUserRole != 4">{{ calc.buyer_c3_cost }} ₽</div>
    </div>
    <div class="calc-table__row line-hover" v-show="calc.dirt">
      <div class="calc-table__cell">Грязь</div>
      <div class="calc-table__cell">{{ calc.dirt }}</div>
      <div class="calc-table__cell" v-show="currentUserRole != 4">{{ calc.seller_dirt_cost }} ₽</div>
      <div class="calc-table__cell" v-show="currentUserRole != 4">{{ calc.buyer_dirt_cost }} ₽</div>
    </div>
  </div>
</template>

<script>
 export default {
  name: "CalcTable",
  props: ['calc'],
  data() {
    return {
      currentUserRole: localStorage.getItem('userRole'),
    }
  }
}
</script>

<style lang="scss" scoped>
form {
  font-family: 'Montserrat';
}

.table {
  text-align: center;
  border: solid #ebebeb 3px;
  margin-bottom: 1rem;

  &__title {
    background-color: #f5f5f5;
  }
}

td {
  font-weight: 400;
}

.calc-table {
  display: flex;
  flex-direction: column;
  flex-flow: column;
  border: solid 2px #f3f3f3;
  border-radius: 15px;
  padding: 5px 10px;
  background-color: #fff;
  margin-bottom: 5px;

  &__title {
    width: 100%;
    height: 40px;
    margin: 0 auto;
    justify-content: center;
    align-items: center;
    font-size: 20px;
    font-weight: 600;
    border: solid 2px #f3f3f3;
    border-bottom: 0;
    border-radius: 10px;
    background-color: #fff;
  }
  &__text {
    color: #c4c4c4;
  }
  &__row {
    width: 100%;
    display: inline-flex;
    justify-content: space-around;
    margin-bottom: 5px;
    gap: 3px;
  }
  &__cell {
    width: 25%;
    text-align: center;
    border-bottom: solid 1.5px #eeeeee;
    border-radius: 5px;
  }
}

.line-hover {
  &:hover {
    background-color: #f5f5f5;
    border-radius: 5px;
  }
}
</style>
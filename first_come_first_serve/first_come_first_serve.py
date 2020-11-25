from iconservice import *

TAG = 'FirstComeFirstServe'


class FirstComeFirstServe(IconScoreBase):

    
    _ADDRESS_ARRAY = "ADDRESS_ARRAY"
    _TRANSACTION_HASH_ARRAY = "TRANSACTION_HASH_ARRAY"
    _MAX = "MAX"

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._max = VarDB(self._MAX, db, value_type=int)
        self._address_array = ArrayDB(self._ADDRESS_ARRAY, db, value_type=Address)
        self._trasaction_hash_array = ArrayDB(self._TRANSACTION_HASH_ARRAY, db, value_type=str)
        
        

    def on_install(self) -> None:
        super().on_install()
        
        self._max.set(5)
        

    def on_update(self) -> None:
        super().on_update()


    @payable
    @external
    def apply(self):
        Logger.info(f'apply transaction is called - {self.tx.timestamp}', TAG)
        
        if self.msg.sender in self._address_array:
            revert("You already participated")
        
        if len(self._address_array) < self._max.get():
            if self.msg.sender is not None:
                
                self._address_array.put(self.msg.sender)

                json_result = {}
                json_result['index'] = self.tx.index
                json_result['nonce'] = self.tx.nonce
                json_result['from'] = str(self.tx.origin)
                json_result['timestamp'] = self.tx.timestamp
                json_result['txHash'] = bytes.hex(self.tx.hash)
                json_result['amount'] = self.msg.value

                self._trasaction_hash_array.put(str(json_result))
                
        else:
            revert("It's already over")
        

    @external(readonly=True)
    def get_results(self) -> dict:
        Logger.info('get_results called success', TAG)
        
        result = []
        
        for data in self._trasaction_hash_array:
            result.append(data)

        return {"result": result}
import smartpy as sp

FA2 = sp.io.import_stored_contract("modifiedNFT")

class NFT(FA2.FA2):
    pass

class PlentyNFT(sp.Contract):
    FA2MintParam = sp.TRecord(
        address = sp.TAddress,
        amount = sp.TNat,
        metadata = sp.TMap(sp.TString, sp.TBytes),
        token_id = sp.TNat,
    )
    def __init__(self,_admin,_developer,_templateIPFSPath, ):   
        self.init(
            # contract's storage
            admin = _admin,
            developer = _developer,

            paused = sp.bool(False),
            maxSupply = sp.nat(1000),
            price = sp.tez(0),
            templateIPFSPath = _templateIPFSPath, #update path

            mintIndex = sp.nat(0),
            nAirdropped = sp.nat(0),

            #to store who has minted
            ledger = sp.big_map(
                tkey = sp.TAddress,
                tvalue = sp.TNat,
            ),

            #to store discord id of minters
            discord = sp.big_map(
                tkey = sp.TString,
                tvalue = sp.TNat,
            ),

            fa2 = sp.none,

            metadata = sp.big_map({
            "": sp.utils.bytes_of_string("tezos-storage:content"),
            "content": sp.utils.bytes_of_string("""{"name": "Plenty Discord NFT" , "description : Crowdsale Contract that mints NFTs via Plenty Discord Bot" , "admin" : "tz1X7EJX7Q2oBjM2Hur53qmB6yCJmPxttT3h" , "author" : "pichkari&gamma" , "homepage" : "https://tarunsh.com/"}"""),
        })
        
        )
    #UTILITIES
    def string_of_nat(self, params):
       c   = sp.map({x : str(x) for x in range(0, 10)})
       x   = sp.local('x', params)
       res = sp.local('res', [])
       sp.if x.value == 0:
           res.value.push('0')
       sp.while 0 < x.value:
           res.value.push(c[x.value % 10])
           x.value //= 10
       return sp.concat(res.value)

    def checkAdmin(self):
        sp.verify(sp.sender == self.data.admin, message = "Not Admin")
    
    def checkPaused(self):
        sp.verify(self.data.paused == False, message= "Minting is Paused")
    
    @sp.entry_point
    def registerFA2(self, fa2):
        self.checkAdmin()
        self.data.fa2 = sp.some(fa2)

    @sp.entry_point
    def togglePause(self):
        self.checkAdmin()
        self.data.paused = ~self.data.paused

    @sp.entry_point
    def mintNFT(self , params):
        #checks before we mint
        self.checkPaused()
        self.checkAdmin()
        sp.verify(self.data.mintIndex < self.data.maxSupply)
        sp.verify((self.data.ledger.contains(params.address))==False , message = "User Already Has an Existing NFT")
        sp.verify((self.data.discord.contains(params.discord))==False , message = "User Already Has an Existing NFT")

        #mint and send it to addy

        mintData = sp.record(
            address = params.address,
            amount = sp.nat(1),
            metadata = sp.map({
                "": sp.pack(
                    self.data.templateIPFSPath + \
                    self.string_of_nat(self.data.mintIndex) + ".json"
                )
            }),
            token_id = self.data.mintIndex,
        )
        contract = sp.contract(
            self.FA2MintParam,
            self.data.fa2.open_some("NOT_A_VALID_FA2_CONTRACT"),
            'mint'
        ).open_some("WRONG_FA2_CONTRACT")

        sp.transfer(mintData, sp.mutez(0), contract)

        #Increase out counters and update ledger
        self.data.mintIndex += 1
        self.data.nAirdropped +=1

        self.data.ledger[params.address] = 1
        self.data.discord[params.discord] = 1

@sp.add_test("PlentyNFT")
def test():

    #update ipfs
    baseIPFSUrl = "ipfs://QmSscmKnfMkYFKjrubbmrPUdkhATC4gZHktRRamCGyNN3G/"
    admin = sp.test_account("admin")
    bob = sp.test_account("bob")

    scenario = sp.test_scenario()

    plenty = PlentyNFT(
        _admin = admin.address,
        _developer = bob.address , 
        _templateIPFSPath = baseIPFSUrl,
        )



    token = NFT(
        config = FA2.FA2_config(
            non_fungible=True,
            assume_consecutive_token_ids = False
        ),
        admin = admin.address,
        crowdsale = plenty.address,
        metadata = sp.big_map({
            "": sp.utils.bytes_of_string("tezos-storage:content"),
            "content": sp.utils.bytes_of_string("""{"name": "Plenty NFT Contract", "description": "NFT contract for the Plenty Discord Bot"}"""),
        })
    )
    
    scenario += token
    scenario += plenty

    scenario.h2("Registering FA2 contract for our crowdsale.")
    plenty.registerFA2(token.address).run(sender=admin)

    params = sp.record(address = bob.address , discord="123identity")

    scenario += plenty.mintNFT(params).run(sender = admin)
    scenario += plenty.mintNFT(params).run(sender = admin , valid = False)


    #Compilation

    baseIPFSUrl = "ipfs://QmeTmDH6xXdEBGmMBjE15q6MUc33xDgmUec19ouBmqS327/"
    admin = sp.address("tz1X7EJX7Q2oBjM2Hur53qmB6yCJmPxttT3h")
    developer = sp.address("tz1X7EJX7Q2oBjM2Hur53qmB6yCJmPxttT3h")

    sp.add_compilation_target("Plenty", PlentyNFT(
    _admin = admin,
    _developer = developer,
    # _maxSupply = sp.nat(10000),
    _templateIPFSPath = baseIPFSUrl,))

    #update
    crowdsale = sp.address("KT1RPeo9eQ4inwmvPC6Ma3SWVe3rGeBuc4S4")

    sp.add_compilation_target("Token", NFT(
        config = FA2.FA2_config(
            non_fungible=True,
            assume_consecutive_token_ids = False
        ),
        admin = admin,
        crowdsale = crowdsale,
        metadata = sp.big_map({
            "": sp.utils.bytes_of_string("tezos-storage:content"),
            "content": sp.utils.bytes_of_string("""{"name": "Plenty Discord NFT" , "description : A FA2 Contract that stores the NFT's minted via Plenty Discord Bot" , "version" : "FA2" , "author" : "pichkari&gamma" , "homepage" : "https://tarunsh.com/" , "interfaces" : "https://gitlab.com/tezos/tzip/-/tree/master/proposals/tzip-16" }"""),
        })
    ))



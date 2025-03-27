Fork of https://github.com/ethereum/staking-deposit-cli.

## Warning DO NOT USE IN PRODUCTION

I added the ability to dynamically generate stakers and passwords, then output the files to a mounted directory. 

### Usage
```
docker run -i --rm -v ./stakers:/tmp ghcr.io/admiraladmirable/staking-deposit-cli:<tag> <num-stakers>

```

### Example
```
mkdir stakers
docker run -i --rm -v ./stakers:/tmp ghcr.io/admiraladmirable/staking-deposit-cli:v0.1.2 4
sudo chown -R "$USER": stakers

```

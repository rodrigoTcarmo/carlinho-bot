git describe --tags --abbrev=0 | awk -F. \'{print substr($1,2)"."$2"."$3+1}\'

for l in ${CURRENT_VERSION}; do
  echo l
done

echo "${CURRENT_VERSION}"

function pause() {
  read -s  -n 1 -p "Press any key to continue..."
  echo ""
}

pause